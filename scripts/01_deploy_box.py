from scripts.helpful_scripts import get_account, encode_function_data
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})

    proxy_admin = ProxyAdmin.deploy({"from": account})

    # initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gaz_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade to v2")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(45, {"from": account})
    print(proxy_box.retrieve())
