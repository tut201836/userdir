import yaml
import os
import random
import math

def generate_choreonoid_body_and_spring_settings(x_joint_count=10, z_joint_count=10, joint_width=0.2, body_filename="step_floor.body", spring_filename="SpringCustomizerSettings.yaml"):
    # Bodyファイルの基本構造
    body_data = {
        "format": "ChoreonoidBody",
        "format_version": 2.0,
        "angle_unit": "degree",
        "name": "step_floor",
        "root_link": "Base",
        "links": [
            {
                "name": "Base",
                "elements": [
                    {
                        "type": "Transform",
                        "elements": [
                            {
                                "type": "Transform",
                                "translation": [-2.3, 0, -0.05],
                                "elements": [
                                    {
                                        "type": "Shape",
                                        "appearance": {
                                            "material": {
                                                "diffuse": [0.14, 0, 0.35],
                                                "emissive": [0.06, 0, 0.15],
                                            }
                                        },
                                        "geometry": {
                                            "type": "Box",
                                            "size": [5, 10, 0.1],
                                        },
                                    }
                                ],
                            }
                        ],
                    }
                ],
                "joint_name": "Base",
                "joint_type": "free",
                "mass": 5000,
                "center_of_mass": [-2.5, 0, -0.05],
                "inertia": [
                    41670.8, 0, 0,
                    0, 10420.8, 0,
                    0, 0, 10833.3,
                ],
            }
        ],
    }

    # Spring設定の基本構造
    spring_settings = {"springs": []}

    # ジョイントの生成と設定の追加
    for i in range(x_joint_count):
        for j in range(z_joint_count):
            joint_name = f"joint{i}_{j}"
            translation_value = [i * 0.5, 0, j * joint_width]
            shape_translation = [0.3 + i * joint_width, 0, (-joint_width * 0.5) + j * (-joint_width)]

            # 格子状に色を変更する設定
            if (i + j) % 2 == 0:
                diffuse_color = [0, 0.49, 0.49]
                emissive_color = [0, 0.21, 0.21]
            else:
                diffuse_color = [0, 0, 0.49]
                emissive_color = [0, 0, 0.21]

            # 波状の起伏をy軸方向に設定
            wave_amplitude = 0.1  # 高さの振幅
            wave_frequency = 0.5  # 波の周波数（小さいほど周期が長くなる）
            height_variation = wave_amplitude * math.sin(wave_frequency * i) * math.cos(wave_frequency * j)

            # ランダムで回転か沈むジョイントを選択
            if random.choice([True, False]):
                joint_type = "revolute"
                joint_axis = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
                joint_range = [-3.14, 3.14]  # 回転範囲
            else:
                joint_type = "prismatic"
                joint_axis = [0, 1, 0]  # y軸方向に沈む
                joint_range = [-0.1, 0.1]  # 上下方向の範囲

            # ジョイントの定義
            joint = {
                "name": joint_name,
                "elements": [
                    {
                        "type": "Transform",
                        "rotation": [-1, 0, 0, 90],
                        "translation": [0.1 + (-i * 0.51), height_variation, (j * (joint_width + 0.01)) - (0.5 * joint_width * z_joint_count)],
                        "elements": [
                            {
                                "type": "Transform",
                                "translation": shape_translation,
                                "elements": [
                                    {
                                        "type": "Shape",
                                        "appearance": {
                                            "material": {
                                                "diffuse": diffuse_color,
                                                "emissive": emissive_color,
                                            }
                                        },
                                        "geometry": {
                                            "type": "Box",
                                            "size": [joint_width, joint_width, joint_width],
                                        },
                                    }
                                ],
                            }
                        ],
                    }
                ],
                "parent": "Base",
                "translation": translation_value,
                "rotation": [1, 0, 0, 90],
                "joint_name": joint_name,
                "joint_type": joint_type,
                "joint_axis": joint_axis,
                "joint_id": i,
                "joint_range": joint_range,
                "joint_axis_inertia": 1,
                "mass": 0.005,
                "center_of_mass": [1.0 + (-i * 0.5), height_variation, (j * joint_width) - (z_joint_count * joint_width * 0.5)],
                "inertia": [
                    0.0420833, 0, 0,
                    0, 0.00427083, -8.32667e-19,
                    0, -8.32667e-19, 0.000520833,
                ],
            }

            # ジョイントをBodyデータに追加
            body_data["links"].append(joint)

            # Spring設定に速度制限を追加
            spring_setting = {
                "joint_name": joint_name,
                "K": 2000,
                "D": 2000,
                "upper_limit": joint_range[1],
                "lower_limit": joint_range[0],
                "velocity_limit": 20.0,  # 最大速度の制限
            }

            # Spring設定をSpringデータに追加
            spring_settings["springs"].append(spring_setting)

    try:
        # Bodyファイルの生成
        with open(body_filename, "w") as body_file:
            yaml.dump(body_data, body_file, default_flow_style=False, sort_keys=False, indent=2)
        print(f"Bodyファイル '{body_filename}' を生成しました。ジョイント数: {x_joint_count}、幅: {joint_width}")

        # SpringCustomizerSettings.yamlの生成
        with open(spring_filename, "w") as spring_file:
            yaml.dump(spring_settings, spring_file, default_flow_style=False, sort_keys=False, indent=2)
        print(f"Spring設定ファイル '{spring_filename}' を生成しました。")

    except Exception as e:
        print(f"ファイルの生成中にエラーが発生しました: {e}")

# スクリプトの実行例
if __name__ == "__main__":
    generate_choreonoid_body_and_spring_settings(x_joint_count=15, z_joint_count=5, joint_width=0.3)
