def load(shell):
    import os

    def l():
        files = os.listdir()
        print(f"Total: {len(files)} / {shell.state['origen']}\n")
        for f in files:
            path = os.path.join(os.getcwd(), f)

            if os.path.isdir(path):
                print(f"\033[34m[D] {f}/\033[0m")   # azul carpetas
            else:
                try:
                    size = os.path.getsize(path)
                    print(f"\033[32m[∆] {f}\033[0m")   # verde archivos
                except:
                    print(f"\033[32m[∆] {f}\033[0m")   # verde archivos

    shell.register_command("l", l)
