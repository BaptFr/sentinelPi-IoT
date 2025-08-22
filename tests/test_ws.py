import asyncio
import websockets
from websockets.exceptions import ConnectionClosed

RPI_DEVICE_ID = "serrure1"
WS_URI = f"wss://sentinelpi.tech/ws/raspberry/{RPI_DEVICE_ID}"

async def test_ws():
    ws = None
    try:
        ws = await websockets.connect(WS_URI, ping_interval=None)
        print("[WS] Connecté au serveur")

        await ws.send("Hello from Raspberry Pi")
        print("[WS] Message envoyé")

        try:
            response = await ws.recv()
            print(f"[WS] Message reçu : {response}")
        except ConnectionClosed:
            print("[WS] Connexion fermée par le serveur sans close frame")

    except Exception as e:
        print(f"[WS] Erreur : {e}")
    finally:
        if ws:
            # Ferme le transport de force pour éviter l'erreur close frame
            ws.transport.close()
            print("[WS] Connexion fermée côté client (de force)")

if __name__ == "__main__":
    asyncio.run(test_ws())
