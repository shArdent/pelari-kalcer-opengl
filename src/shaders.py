from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *
import sys

VERTEX_SHADER_SCENE = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

out vec3 FragPos;
out vec3 Normal;
out vec4 FragPosLightSpace;
out vec4 FragPosMoonSpace;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 lightSpaceMatrix;
uniform mat4 moonSpaceMatrix;

void main()
{
    FragPos = vec3(model * vec4(aPos, 1.0));
    Normal = transpose(inverse(mat3(model))) * aNormal;
    FragPosLightSpace = lightSpaceMatrix * vec4(FragPos, 1.0);
    FragPosMoonSpace = moonSpaceMatrix * vec4(FragPos, 1.0);
    gl_Position = projection * view * vec4(FragPos, 1.0);
}
"""

FRAGMENT_SHADER_SCENE = """
#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;
in vec4 FragPosLightSpace;
in vec4 FragPosMoonSpace;

uniform sampler2D shadowMap;
uniform sampler2D moonShadowMap;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 objectColor;
uniform vec3 lightColor;
uniform vec3 moonDir;
uniform vec3 moonColor;
uniform int isGround;

float ShadowCalculation(vec4 fragPosSpace, sampler2D map, vec3 lightD)
{
    if (fragPosSpace.w <= 0.0) return 0.0;
    vec3 projCoords = fragPosSpace.xyz / fragPosSpace.w;
    projCoords = projCoords * 0.5 + 0.5;
    if(projCoords.z > 1.0 || projCoords.x < 0.0 || projCoords.x > 1.0 || projCoords.y < 0.0 || projCoords.y > 1.0)
        return 0.0;
    float currentDepth = texture(map, projCoords.xy).r; 
    float currentZ = projCoords.z;
    vec3 normal = normalize(Normal);
    float bias = max(0.0005 * (1.0 - dot(normal, lightD)), 0.00005);
    float shadow = 0.0;
    vec2 texelSize = 1.0 / textureSize(map, 0);
    for(int x = -1; x <= 1; ++x) {
        for(int y = -1; y <= 1; ++y) {
            float pcfDepth = texture(map, projCoords.xy + vec2(x, y) * texelSize).r; 
            shadow += currentZ - bias > pcfDepth  ? 1.0 : 0.0;        
        }    
    }
    shadow /= 9.0;
    return shadow;
}

void main()
{
    vec3 color = objectColor;
    
    if (isGround == 1) {
        float a = 25.0;
        float b = 15.0;
        float val = sqrt((FragPos.x * FragPos.x) / (a * a) + (FragPos.z * FragPos.z) / (b * b));
        vec3 trackColor = vec3(0.6, 0.15, 0.1); 
        vec3 lineColor = vec3(1.0, 1.0, 1.0);   
        if (val > 0.85 && val < 1.15) {
            color = trackColor;
            float trackProgress = (val - 0.85) / 0.3;
            float numLanes = 4.0;
            float lineThickness = 0.03; 
            float laneCoord = fract(trackProgress * numLanes);
            if (laneCoord < lineThickness || laneCoord > 1.0 - lineThickness) {
                color = mix(trackColor, lineColor, 0.8);
            }
            if (trackProgress < 0.02 || trackProgress > 0.98) {
                color = lineColor;
            }
        } else if (val <= 0.85) {
            color = vec3(0.2, 0.55, 0.2);
        } else {
            color = vec3(0.15, 0.45, 0.15);
        }
    }

    vec3 normal = normalize(Normal);
    vec3 lightD = normalize(lightPos - FragPos);
    
    // Spotlight
    vec3 spotDir = normalize(vec3(0.0, 0.0, 0.0) - lightPos); 
    float theta = dot(-lightD, spotDir); 
    float cutOff = cos(radians(35.0));
    float outerCutOff = cos(radians(55.0));
    float epsilon = cutOff - outerCutOff;
    float intensity = clamp((theta - outerCutOff) / epsilon, 0.0, 1.0);
    
    // Moonlight
    vec3 mDir = normalize(-moonDir);
    float mDiff = max(dot(normal, mDir), 0.0);
    vec3 mDiffuse = mDiff * moonColor;
    
    vec3 mSpecular = vec3(0.0);
    if (isGround == 0) {
        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-mDir, normal);
        float mSpec = pow(max(dot(viewDir, reflectDir), 0.0), 16.0);
        mSpecular = 0.2 * mSpec * moonColor;
    }

    // Ambient
    float ambientStrength = 0.2;
    vec3 ambient = ambientStrength * moonColor;
    
    // Diffuse
    float diff = max(dot(normal, lightD), 0.0);
    vec3 diffuse = diff * lightColor * intensity;
    
    // Specular
    vec3 specular = vec3(0.0);
    if (isGround == 0) { 
        float specularStrength = 0.2;
        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-lightD, normal);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 16.0);
        specular = specularStrength * spec * lightColor * intensity;
    }
    
    // Shadows
    float shadow = ShadowCalculation(FragPosLightSpace, shadowMap, lightD);       
    float mShadow = ShadowCalculation(FragPosMoonSpace, moonShadowMap, mDir);
    
    vec3 spotLighting = (1.0 - shadow) * (diffuse + specular);
    vec3 moonLighting = (1.0 - mShadow) * (mDiffuse + mSpecular);
    
    vec3 lighting = (ambient + spotLighting + moonLighting) * color;    
    
    FragColor = vec4(lighting, 1.0);
}
"""

VERTEX_SHADER_DEPTH = """
#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 lightSpaceMatrix;
uniform mat4 model;

void main()
{
    gl_Position = lightSpaceMatrix * model * vec4(aPos, 1.0);
}
"""

FRAGMENT_SHADER_DEPTH = """
#version 330 core
void main()
{
    // gl_FragDepth = gl_FragCoord.z;
}
"""



def compile_all_shaders():
    try:
        scene_shader = compileProgram(
            compileShader(VERTEX_SHADER_SCENE, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER_SCENE, GL_FRAGMENT_SHADER)
        )
        depth_shader = compileProgram(
            compileShader(VERTEX_SHADER_DEPTH, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER_DEPTH, GL_FRAGMENT_SHADER)
        )
        return scene_shader, depth_shader
    except Exception as e:
        print(f"Shader compilation failed: {e}")
        sys.exit(1)
