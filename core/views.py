# core/views.py
from django.shortcuts import render
from .models import WalletStat
from web3 import Web3

# Haust RPC
RPC_URL = "https://rpc-testnet.haust.app"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_wallet_transactions(wallet):
    """Fetch transaction count for a wallet using Haust RPC"""
    try:
        return w3.eth.get_transaction_count(wallet)
    except Exception as e:
        print("Error fetching txns:", e)
        return 0

def index(request):
    stats = {"transactions": "-", "level": "-", "rank": "-"}
    
    if request.method == "POST":
        wallet = request.POST.get("wallet_address")
        if wallet:
            # get txn count
            txn_count = get_wallet_transactions(wallet)

            # save/update wallet stats
            wallet_stat, _ = WalletStat.objects.update_or_create(
                wallet_address=wallet,
                defaults={"transactions": txn_count},
            )

            # determine level
            level = wallet_stat.get_level()

            # determine rank (based on wallets stored in DB)
            all_wallets = WalletStat.objects.order_by("-transactions")
            ranks = {w.wallet_address: idx + 1 for idx, w in enumerate(all_wallets)}
            rank = ranks.get(wallet, "-")

            stats = {
                "transactions": txn_count,
                "level": level,
                "rank": f"#{rank}",
            }

    return render(request, "core/index.html", {"stats": stats})
