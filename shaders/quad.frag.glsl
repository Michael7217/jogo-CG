#version 330 compatibility

in vec4 v_color;
in vec2 v_texcoord;
out vec4 fragColor;

uniform bool u_use_texture;
uniform sampler2D u_texture;

void main() {
    if (u_use_texture) {
        fragColor = texture(u_texture, v_texcoord) * v_color;
    } else {
        fragColor = v_color;
    }
}
