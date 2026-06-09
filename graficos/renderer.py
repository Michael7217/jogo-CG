import ctypes
from pathlib import Path

from PIL import Image
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_DYNAMIC_DRAW,
    GL_STATIC_DRAW,
    GL_FALSE,
    GL_FLOAT,
    GL_LINES,
    GL_LINEAR,
    GL_LINEAR_MIPMAP_LINEAR,
    GL_MODELVIEW,
    GL_MODELVIEW_MATRIX,
    GL_PROJECTION_MATRIX,
    GL_REPEAT,
    GL_RGBA,
    GL_TEXTURE_2D,
    GL_TEXTURE0,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_TRIANGLES,
    GL_UNSIGNED_BYTE,
    glActiveTexture,
    glBindBuffer,
    glBindTexture,
    glBindVertexArray,
    glBufferData,
    glDrawArrays,
    glPushMatrix,
    glPopMatrix,
    glTranslatef,
    glScalef,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenerateMipmap,
    glGenTextures,
    glGenVertexArrays,
    glDeleteBuffers,
    glDeleteVertexArrays,
    glGetFloatv,
    glGetUniformLocation,
    glLoadIdentity,
    glMatrixMode,
    glTexImage2D,
    glTexParameteri,
    glUniform1i,
    glUniformMatrix4fv,
    glUseProgram,
    glVertexAttribPointer,
    glRotatef
)
from config.config import (
    LARGURA_TELA, ALTURA_TELA,
    TAMANHO_BLOCO, TIPO_BLOCO_SOLO, TIPO_BLOCO_PAREDE,
    TIPO_BLOCO_AGUA, TIPO_BLOCO_BURACO,
    TIPO_BLOCO_ACUDE, TIPO_BLOCO_POCO,
    TIPO_BLOCO_CACIMBA, TIPO_BLOCO_DISPUTA,
)
from graficos.conversoes import bloco_para_mundo


class Renderizador3D:
    def __init__(self, programa_shader):
        self.programa = programa_shader
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.textura_chao = self._carregar_textura_chao()
        self.textura_aldeao = self._carregar_textura_aldeao()
        self.models = {}
        self._model_drawn_once = {}
        self._carregar_modelos_disponiveis()

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, 0, None, GL_DYNAMIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0,
            3,
            GL_FLOAT,
            GL_FALSE,
            9 * ctypes.sizeof(ctypes.c_float),
            ctypes.c_void_p(0)
        )

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1,
            4,
            GL_FLOAT,
            GL_FALSE,
            9 * ctypes.sizeof(ctypes.c_float),
            ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float))
        )

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(
            2,
            2,
            GL_FLOAT,
            GL_FALSE,
            9 * ctypes.sizeof(ctypes.c_float),
            ctypes.c_void_p(7 * ctypes.sizeof(ctypes.c_float))
        )

        glBindVertexArray(0)

        self._loc_projection = glGetUniformLocation(self.programa, b"u_projection")
        self._loc_view = glGetUniformLocation(self.programa, b"u_view")
        self._loc_use_texture = glGetUniformLocation(self.programa, b"u_use_texture")
        self._loc_texture = glGetUniformLocation(self.programa, b"u_texture")

        glUseProgram(self.programa)
        if self._loc_projection != -1:
            proj = glGetFloatv(GL_PROJECTION_MATRIX)
            glUniformMatrix4fv(self._loc_projection, 1, GL_FALSE, proj)
        if self._loc_texture != -1:
            glUniform1i(self._loc_texture, 0)
        glUseProgram(0)

    def _carregar_modelos_disponiveis(self):
        modelos_dir = Path(__file__).resolve().parent.parent / "models"
        candidatos = {
            "aldeao": modelos_dir / "aldeano.obj",
        }

        for nome, caminho in candidatos.items():
            if caminho.exists():
                try:
                    entry = self._carregar_modelo_obj(caminho)
                    self.models[nome] = entry
                    meshes = entry.get("meshes", [])
                    total = sum(m[2] for m in meshes) if meshes else 0
                    print(f"[renderer] modelo '{nome}' carregado: {len(meshes)} meshes, {total} vertices")
                except Exception as e:
                    self.models[nome] = None
                    print(f"[renderer] falha ao carregar modelo '{nome}': {e}")

    def _carregar_modelo_obj(self, caminho: Path):
        try:
            text = caminho.read_text(encoding='utf-8')
        except Exception:
            text = caminho.read_text(encoding='latin-1')

        vertices_raw = []
        uvs_raw = []
        
        converted = []
        positions = []

        for line in text.splitlines():
            line = line.strip()
            # Ignora comentários e linhas vazias
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if not parts:
                continue
                
            tipo = parts[0]
            
            if tipo == 'v':
                # Coordenadas do vértice
                vertices_raw.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif tipo == 'vt':
                # Coordenadas de textura (UV)
                uvs_raw.append((float(parts[1]), float(parts[2])))
            elif tipo == 'f':
                # Lida com faces (Triângulos ou Quads) e converte para triângulos
                face_verts = parts[1:]
                
                # Triangulação em leque (fan) - resolve faces com 3, 4 ou mais lados
                for i in range(1, len(face_verts) - 1):
                    for idx in (0, i, i + 1):
                        # Pega o bloco "v/vt/vn" ou "v//vn" ou "v"
                        v_data = face_verts[idx].split('/')
                        
                        # Arrays em Python começam em 0, mas no OBJ começam em 1
                        v_idx = int(v_data[0]) - 1
                        x, y, z = vertices_raw[v_idx]
                        
                        u, v = 0.0, 0.0
                        # Se o modelo possuir mapeamento de textura (UV)
                        if len(v_data) > 1 and v_data[1]:
                            vt_idx = int(v_data[1]) - 1
                            u, v = uvs_raw[vt_idx]
                            
                        # Adiciona no formato que o seu VBO espera: x, y, z, r, g, b, a, u, v
                        converted.extend([x, y, z, 1.0, 1.0, 1.0, 1.0, u, v])
                        positions.append((x, y, z))

        # Se não carregou nada, retorna modelo vazio
        if not converted:
            return {"meshes": [], "scale": 1.0}

        # --- Criação do VAO e VBO (seu código original mantido) ---
        array = (ctypes.c_float * len(converted))(*converted)
        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(array), array, GL_STATIC_DRAW)

        # Atributo 0: Posição
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        # Atributo 1: Cor
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        # Atributo 2: Coordenadas de Textura
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(7 * ctypes.sizeof(ctypes.c_float)))

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # 9 floats por vértice
        vertex_count = len(converted) // 9
        meshes = [(vao, vbo, vertex_count)]

        # --- Cálculo do Bounding Box e Escala ---
        if positions:
            xs = [p[0] for p in positions]
            ys = [p[1] for p in positions]
            zs = [p[2] for p in positions]
            dx = max(xs) - min(xs)
            dy = max(ys) - min(ys)
            dz = max(zs) - min(zs)
            max_extent = max(dx, dy, dz, 1e-6)
            suggested_scale = TAMANHO_BLOCO / max_extent
        else:
            suggested_scale = 1.0

        return {"meshes": meshes, "scale": suggested_scale}

    def desenhar_modelo(self, nome, camera, mundo_x, mundo_y, mundo_z=0.0, escala=1.0):
        entry = self.models.get(nome)
        if not entry:
            return

        if not self._model_drawn_once.get(nome):
            print(f"[renderer] desenhando modelo '{nome}' pela primeira vez")
            self._model_drawn_once[nome] = True

        meshes = entry.get("meshes")
        model_scale = entry.get("scale", 1.0)
        final_scale = escala * model_scale

        # Ativa o programa shader
        glUseProgram(self.programa)

        # Configura matriz de modelo + câmera
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        camera.aplicar_transformacao()
        glTranslatef(mundo_x, mundo_y, mundo_z)
        glRotatef(90, 1.0, 0.0, 0.0)
        glScalef(final_scale, final_scale, final_scale)

        # Atualiza a uniform da view com a matriz atual
        if self._loc_view != -1:
            view = glGetFloatv(GL_MODELVIEW_MATRIX)
            glUniformMatrix4fv(self._loc_view, 1, GL_FALSE, view)

        tem_textura = False
        if nome == 'aldeao' and hasattr(self, 'textura_aldeao') and self.textura_aldeao is not None:
            tem_textura = True

        # Avisa o seu Shader que ele deve usar textura (u_use_texture = 1)
        if self._loc_use_texture != -1:
            glUniform1i(self._loc_use_texture, 1 if tem_textura else 0)
            
        if tem_textura:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.textura_aldeao)

        # Desenha cada mesh do modelo
        for vao, vbo, count in meshes:
            glBindVertexArray(vao)
            glDrawArrays(GL_TRIANGLES, 0, count)
            glBindVertexArray(0)

        # ====== DESLIGA A TEXTURA ======
        if tem_textura:
            glBindTexture(GL_TEXTURE_2D, 0)
            
        if self._loc_use_texture != -1:
            glUniform1i(self._loc_use_texture, 0) # Volta para o modo de cor sólida

        glPopMatrix()
        glUseProgram(0)
        
        # Restaura a view uniform com transformação de câmera apenas
        self._atualizar_matrizes(camera)

    def _carregar_textura_chao(self):
        diretorio_texturas = Path(__file__).resolve().parent.parent / "texturas"
        candidatos = [
            diretorio_texturas / "sandy_gravel_02_diff_4k.jpg",
            diretorio_texturas / "sandy_gravel_02_diff_4k.jpeg",
            diretorio_texturas / "sandy_gravel_02_diff_4k.png",
        ]

        caminho_textura = next((caminho for caminho in candidatos if caminho.exists()), None)
        if caminho_textura is None:
            return None

        imagem = Image.open(caminho_textura).convert("RGBA")
        imagem = imagem.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        largura, altura = imagem.size
        dados = imagem.tobytes()

        textura = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textura)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            largura,
            altura,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            dados
        )
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        return textura

    def _atualizar_matrizes(self, camera):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera.aplicar_transformacao()

        if self._loc_view != -1:
            view = glGetFloatv(GL_MODELVIEW_MATRIX)
            glUseProgram(self.programa)
            glUniformMatrix4fv(self._loc_view, 1, GL_FALSE, view)
            glUseProgram(0)

    def _enviar_vertices(self, vertices, modo):
        if not vertices:
            return

        buffer = (ctypes.c_float * len(vertices))(*vertices)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(buffer), buffer, GL_DYNAMIC_DRAW)
        glUseProgram(self.programa)
        if self._loc_use_texture != -1:
            glUniform1i(self._loc_use_texture, 0)
        glDrawArrays(modo, 0, len(vertices) // 9)
        glUseProgram(0)
        glBindVertexArray(0)

    def _enviar_vertices_textura(self, vertices, modo, textura=None):
        if not vertices:
            return

        buffer = (ctypes.c_float * len(vertices))(*vertices)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(buffer), buffer, GL_DYNAMIC_DRAW)
        glUseProgram(self.programa)
        if self._loc_use_texture != -1:
            glUniform1i(self._loc_use_texture, 1 if textura else 0)
        if textura:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, textura)
        glDrawArrays(modo, 0, len(vertices) // 9)
        if textura:
            glBindTexture(GL_TEXTURE_2D, 0)
        if self._loc_use_texture != -1:
            glUniform1i(self._loc_use_texture, 0)
        glUseProgram(0)
        glBindVertexArray(0)

    def desenhar_grade(self, grade, camera):
        self._atualizar_matrizes(camera)

        blocos_solo = []
        blocos_disputa = []
        triangulos = []
        linhas = []

        for linha in grade.blocos:
            for bloco in linha:
                mundo_x, mundo_y, mundo_z = bloco_para_mundo(bloco.x, bloco.y)

                self._adicionar_vertices_do_bloco(
                    bloco,
                    mundo_x,
                    mundo_y,
                    mundo_z,
                    blocos_solo,
                    blocos_disputa,
                    triangulos,
                )

                if bloco.destacado:
                    destaque = (0.0, 1.0, 1.0, 0.5)
                    triangulos.extend(self._quads_para_triangulos(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, destaque))

                linhas.extend(self._quads_para_linhas(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, (0.1, 0.1, 0.1, 1.0)))

        self._enviar_vertices_textura(blocos_solo, GL_TRIANGLES, self.textura_chao)
        self._enviar_vertices(triangulos, GL_TRIANGLES)
        self._enviar_vertices(blocos_disputa, GL_TRIANGLES)
        self._enviar_vertices(linhas, GL_LINES)

    def _adicionar_vertices_do_bloco(self, bloco, mundo_x, mundo_y, mundo_z, blocos_solo, blocos_disputa, triangulos):
        if bloco.tipo in (TIPO_BLOCO_SOLO, TIPO_BLOCO_DISPUTA, TIPO_BLOCO_POCO, TIPO_BLOCO_CACIMBA):
            blocos_solo.extend(self._quads_texturizados(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, (1.0, 1.0, 1.0, 1.0)))

        if bloco.tipo == TIPO_BLOCO_DISPUTA:
            blocos_disputa.extend(self._quads_para_triangulos(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, (0.9, 0.2, 0.2, 0.35)))
        elif bloco.tipo == TIPO_BLOCO_POCO:
            triangulos.extend(self._quads_para_triangulos(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, (0.18, 0.12, 0.06, 0.55)))
        elif bloco.tipo == TIPO_BLOCO_CACIMBA:
            triangulos.extend(self._quads_para_triangulos(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, (0.74, 0.58, 0.35, 0.45)))
        elif bloco.tipo == TIPO_BLOCO_ACUDE:
            triangulos.extend(self._quads_para_triangulos(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, (0.12, 0.28, 0.75, 0.92)))
        elif bloco.tipo == TIPO_BLOCO_PAREDE:
            triangulos.extend(self._quads_para_triangulos(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, (0.5, 0.5, 0.5, 1.0)))
        elif bloco.tipo == TIPO_BLOCO_AGUA:
            triangulos.extend(self._quads_para_triangulos(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, (0.1, 0.3, 0.8, 1.0)))
        elif bloco.tipo == TIPO_BLOCO_BURACO:
            triangulos.extend(self._quads_para_triangulos(mundo_x, mundo_y, mundo_z, TAMANHO_BLOCO, (0.0, 0.0, 0.0, 1.0)))

    @staticmethod
    def _quads_para_triangulos(x, y, z, tamanho, cor):
        r, g, b, a = cor
        return [
            x - tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a, 0.0, 0.0,
            x + tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a, 1.0, 0.0,
            x + tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a, 1.0, 1.0,
            x - tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a, 0.0, 0.0,
            x + tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a, 1.0, 1.0,
            x - tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a, 0.0, 1.0,
        ]

    @staticmethod
    def _quads_texturizados(x, y, z, tamanho, cor):
        r, g, b, a = cor
        meio = tamanho * 0.5
        cantos = [
            (-meio, -meio, 0.0, 0.0),
            (meio, -meio, 1.0, 0.0),
            (meio, meio, 1.0, 1.0),
            (-meio, -meio, 0.0, 0.0),
            (meio, meio, 1.0, 1.0),
            (-meio, meio, 0.0, 1.0),
        ]

        vertices = []
        for dx, dy, u, v in cantos:
            vertices.extend([x + dx, y + dy, z, r, g, b, a, u, v])

        return vertices

    @staticmethod
    def _quads_para_linhas(x, y, z, tamanho, cor):
        r, g, b, a = cor
        return [
            x - tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a, 0.0, 0.0,
            x + tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a, 0.0, 0.0,
            x + tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a, 0.0, 0.0,
            x + tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a, 0.0, 0.0,
            x + tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a, 0.0, 0.0,
            x - tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a, 0.0, 0.0,
            x - tamanho * 0.5, y + tamanho * 0.5, z, r, g, b, a, 0.0, 0.0,
            x - tamanho * 0.5, y - tamanho * 0.5, z, r, g, b, a, 0.0, 0.0,
        ]
    
    def _carregar_textura_aldeao(self):
        diretorio_texturas = Path(__file__).resolve().parent.parent / "texturas"
        caminho_textura = diretorio_texturas / "aldeano_Cube.jpg"

        if not caminho_textura.exists():
            print(f"[renderer] Aviso: Textura não encontrada em {caminho_textura}")
            return None

        imagem = Image.open(caminho_textura).convert("RGBA")
        # imagem = imagem.transpose(Image.Transpose.FLIP_TOP_BOTTOM) 
        largura, altura = imagem.size
        dados = imagem.tobytes()

        textura = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textura)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, dados)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        return textura


    def desenhar_unidades(self, gerenciador_unidades, camera):
        """Desenha todas as unidades no tabuleiro como modelos 3D."""
        unidades = gerenciador_unidades.obter_todas_unidades()
        
        for unidade in unidades:
            mundo_x, mundo_y, mundo_z = bloco_para_mundo(unidade.tile_x, unidade.tile_y)
            
            if unidade.selecionado:
                triangulos = self._quads_para_triangulos(
                    mundo_x, mundo_y, mundo_z - 0.05,
                    TAMANHO_BLOCO * 0.8,
                    (1.0, 0.9, 0.0, 0.9)
                )
                self._atualizar_matrizes(camera)
                self._enviar_vertices(triangulos, GL_TRIANGLES)
            
            escala = 0.9 if (hasattr(unidade, 'ja_agiu') and unidade.ja_agiu) else 1.0
            self.desenhar_modelo('aldeao', camera, mundo_x, mundo_y, mundo_z + 0.5, escala=escala)
    
    def desenhar_tiles_alcancaveis(self, tiles_alcancaveis, grade, camera):
        """Destaca tiles alcançáveis (Into the Breach style)."""
        self._atualizar_matrizes(camera)
        
        if not tiles_alcancaveis:
            return
        
        triangulos = []
        for tile_x, tile_y in tiles_alcancaveis:
            bloco = grade.obter_bloco(tile_x, tile_y)
            if bloco:
                mundo_x, mundo_y, mundo_z = bloco_para_mundo(tile_x, tile_y)
                triangulos.extend(self._quads_para_triangulos(
                    mundo_x, mundo_y, mundo_z + 0.05,
                    TAMANHO_BLOCO * 0.95,
                    (0.3, 0.6, 1.0, 0.3)
                ))
        
        if triangulos:
            self._enviar_vertices(triangulos, GL_TRIANGLES)
