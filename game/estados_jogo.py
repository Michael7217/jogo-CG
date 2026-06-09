"""
Estados possíveis do jogo.

Gerencia a máquina de estados do gameplay:
- MODO_SELECAO: esperando seleção de unidade
- MODO_MOVIMENTO: unidade selecionada, aguardando clique para mover
- MODO_ANIMACAO: animação de movimento em progresso
- MODO_TRANSICAO_TURNO: transição entre turnos
"""

from enum import Enum, auto


class EstadoJogo(Enum):
    """Enumeração dos estados possíveis do jogo."""
    
    # Esperando seleção de unidade do jogador atual
    MODO_SELECAO = auto()
    
    # Unidade selecionada, mostrando tiles alcançáveis
    MODO_MOVIMENTO = auto()
    
    # Animando movimento da unidade
    MODO_ANIMACAO = auto()
    
    # Transição entre turnos
    MODO_TRANSICAO_TURNO = auto()
    
    # Jogo pausado
    MODO_PAUSA = auto()
    
    # Jogo finalizado
    MODO_FIM = auto()


class TransicaoEstado:
    """Gerencia transições entre estados do jogo."""
    
    def __init__(self):
        self.estado_atual = EstadoJogo.MODO_SELECAO
        self.tempo_transicao = 0.0
        self.duracao_transicao = 0.5  # segundos
    
    def mudar_estado(self, novo_estado: EstadoJogo):
        """Muda para um novo estado."""
        if self.estado_atual != novo_estado:
            print(f"[Estado] {self.estado_atual.name} → {novo_estado.name}")
            self.estado_atual = novo_estado
            self.tempo_transicao = 0.0
    
    def atualizar(self, delta_tempo: float):
        """Atualiza o tempo de transição."""
        if self.tempo_transicao < self.duracao_transicao:
            self.tempo_transicao += delta_tempo
    
    def transicao_completa(self) -> bool:
        """Retorna True se a transição foi completada."""
        return self.tempo_transicao >= self.duracao_transicao
    
    def progresso_transicao(self) -> float:
        """Retorna o progresso da transição (0.0 a 1.0)."""
        if self.duracao_transicao == 0:
            return 1.0
        return min(1.0, self.tempo_transicao / self.duracao_transicao)
