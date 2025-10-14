from setuptools import find_packages, setup

package_name = "navigator"

_ = setup(
    name=package_name,
    version="1.0.0",
    python_requires=">=3.10",
    packages=find_packages(exclude=["test"]),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        ("share/" + package_name, ["package.xml"]),
    ],
    zip_safe=True,
    entry_points={
        "console_scripts": [
            "navigator_node = navigator_node.main:main",
        ],
    },
)
