
# Spring Customizer

``` bash
export SPRING_CUSTOMIZER_ROBOT=step_floor
export SPRING_CUSTOMIZER_CONF_FILE=$(pwd)/SpringCustomizerSettings.yaml
choreonoid step_world.cnoid
```

## Arguments

- SPRING_CUSTOMIZER_ROBOT

Set robot name to affect this customizer

- SPRING_CUSTOMIZER_CONF_FILE

Yaml file, setting descriptions of spring coefficients

``` yaml
springs:
  - joint_name: <str> ## name of joint
    K: <float> ## Spring coefficient
    D: <float> ## Damping coefficient
    upper_limit: <float> ## upper_limit of joint-angle
    lower_limit: <float> ## lower_limit of joint-angle
  - joint_name: <str>
    K: <float>
    D: <float>
    upper_limit: <float>
    lower_limit: <float>
  - ...
```

## How to use make_step_floor
### How to change the number of lattices
x_joint_count : Number of lattices along x-axis

z_joint_count : Number of lattices along z-axis

joint_width : Joint-to-Joint Width
```
if __name__ == "__main__":
    generate_choreonoid_body_and_spring_settings(x_joint_count=15, z_joint_count=5, joint_width=0.3)
```
