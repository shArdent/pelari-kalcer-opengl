import OpenGL.GL.shaders
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER

VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

out vec3 FragPos;
out vec3 Normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    vec4 worldPos = model * vec4(aPos, 1.0);
    FragPos = worldPos.xyz / worldPos.w;
    Normal = mat3(transpose(inverse(model))) * aNormal;
    gl_Position = projection * view * worldPos;
}
"""

FRAGMENT_SHADER = """
#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;

uniform vec3 viewPos;
uniform bool useLighting;
uniform bool isShadow;
uniform float shadowAlpha;
uniform vec3 overrideColor;

struct SpotLight {
    vec3 position;
    vec3 direction;
    vec3 diffuse;
    vec3 specular;
};

#define NR_SPOT_LIGHTS 4
uniform SpotLight spotLights[NR_SPOT_LIGHTS];

uniform vec3 materialSpecular;
uniform float materialShininess;

vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir) {
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), materialShininess);
    
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (1.0 + 0.01 * distance);
    
    float theta = max(dot(lightDir, normalize(-light.direction)), 0.0);
    float spotEffect = (acos(theta) < radians(80.0)) ? pow(theta, 1.5) : 0.0;
    
    vec3 diffuse = light.diffuse * diff * overrideColor;
    vec3 specular = light.specular * spec * materialSpecular;
    
    return (diffuse + specular) * attenuation * spotEffect;
}

void main() {
    if (isShadow) {
        FragColor = vec4(0.1, 0.15, 0.1, shadowAlpha);
        return;
    }
    
    if (!useLighting) {
        FragColor = vec4(overrideColor, 1.0);
        return;
    }

    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);
    
    vec3 result = vec3(0.35, 0.35, 0.4) * overrideColor;
    
    for(int i = 0; i < NR_SPOT_LIGHTS; i++) {
        result += CalcSpotLight(spotLights[i], norm, FragPos, viewDir);    
    }
    
    FragColor = vec4(result, 1.0);
}
"""

def compile_shaders():
    return OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )
