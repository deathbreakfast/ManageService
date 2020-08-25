from cx_Freeze import setup, Executable


executables = [
        Executable(
            'manageservice/manage-service.py',
            base = None,
            targetName = 'manage-service'
        )
]

setup(
        name='Manage Service',
        version = '1.0.0',
        description = 'A python service that can be used to pull a master branch from GitHub and start it',
        executables = executables
)
