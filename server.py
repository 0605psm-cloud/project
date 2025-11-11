import asyncio
import websockets
from aiohttp import web

# ✅ 웹소켓 핸들러
connected_clients = set()

async def ws_handler(websocket):
    print("✅ WebSocket 클라이언트 연결됨")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"📩 수신: {message}")
            # 받은 메시지를 그대로 브로드캐스트
            for ws in connected_clients:
                if ws != websocket:
                    await ws.send(f"Broadcast: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("❌ WebSocket 연결 종료됨")
    finally:
        connected_clients.remove(websocket)

# ✅ Render용 헬스체크 HTTP 서버
async def healthcheck(request):
    return web.Response(text="Server running OK ✅")

# ✅ 서버 실행
async def main():
    # Render가 요구하는 PORT 환경 변수 가져오기
    import os
    port = int(os.getenv("PORT", 10000))

    # WebSocket 서버는 Render에서 같은 포트 공유 불가하므로 localhost로만 열기
    ws_server = await websockets.serve(ws_handler, "0.0.0.0", port)
    print(f"🚀 WebSocket 서버 실행 중: ws://0.0.0.0:{port}")

    # HTTP 서버는 aiohttp로 실행 (health check 대응)
    app = web.Application()
    app.router.add_get("/", healthcheck)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"🌐 HTTP 헬스체크 서버 실행 중: http://0.0.0.0:{port}")
    await asyncio.Future()  # 무한 대기

if __name__ == "__main__":
    asyncio.run(main())
