#version 430

uniform sampler2D tex;
in vec2 uv;
uniform float blur_size;
out vec4 color;

void main() {
    color = texture(tex, uv).rgba;
    vec4 col = vec4(0.);

    for(float index=0; index<10; index++) {
        vec2 offset_uv = uv + vec2(0, (index/9 - 0.5) * blur_size);
        col += texture(tex, offset_uv);
    }

    col = col / 10;
    col = 1-((1-color)*(1-col));
    color = mix(color, vec4(col.rgb, 1), blur_size*10);
}