import sys
from getopt import getopt
from typing import Dict, List

from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


def main():
    opts = parse_opts(longopts=["project_id", "suffix"])
    validate_opts(opts=opts, required_opts=["project_id", "suffix"])
    create_api_key(opts["project_id"], opts["suffix"])


def create_api_key(project_id: str, suffix: str) -> Key | None:
    """
    Creates and restrict an API key. Add the suffix for uniqueness.

    Args:
        project_id: Google Cloud project id.

    Returns:
        response: Returns the created API Key.
    """
    client = api_keys_v2.ApiKeysClient()

    key = Key()
    key.display_name = f"Translate API Play - {suffix}"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response: Key | None = client.create_key(request=request).result()
    if not response:
        return None

    print(f"Successfully created an API key: {response.name}")
    return response


def validate_opts(opts: Dict[str, str], required_opts: List[str]):
    for required_opt in required_opts:
        if not opts.get(required_opt):
            raise Exception(f"{required_opt} is required")


def parse_opts(shortopts: List[str] = [], longopts: List[str] = []) -> Dict[str, str]:
    argv = sys.argv[1:]
    given_opts = shortopts + longopts
    opts, _ = getopt(argv, ":".join(shortopts) + ":", map_longopts(longopts=longopts))
    opts_dict = {}
    for opt, arg in opts:
        if arg == "":
            continue

        for given_opt in given_opts:
            opt = opt.replace("-", "", 2)
            if opt != given_opt:
                continue

            opts_dict[given_opt] = arg
            break

    return opts_dict


def map_longopts(longopts: List[str]) -> List[str]:
    opts: List[str] = []
    for longopt in longopts:
        opts.append(f"{longopt}=")

    return opts


if __name__ == "__main__":
    main()
