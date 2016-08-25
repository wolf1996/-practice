import module
import argparse
import os.path as opath

def main():
    app = module.App()
    parser = argparse.ArgumentParser(description="Some description")
    parser.add_argument("path", type=module.exist, help="path to codebase")
    parser.add_argument("--config", help="path to config file")
    parser.add_argument("--workdir", help="path to config file")
    parsed = parser.parse_args()
    if parsed.config:
        app.load_config_from_file(parsed.config)
    if parsed.workdir:
        app.set_workdir(parsed.workdir)
    res = app.get_res(parsed.path)
    for i in res:
        buf = module.App.str_elem(i)
        print(buf)
        print("#######################################")




if __name__ == '__main__':
    main()
