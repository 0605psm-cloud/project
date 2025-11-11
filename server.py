import asyncio
import websockets
from aiohttp import web

connected_clients = set()

# ✅ WebSocket 핸들러
async def ws_handler(websocket):
    print("✅ WebSocket 클라이언트 연결됨")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"📩 수신: {message}")
            for ws in connected_clients:
                if ws != websocket:
                    await ws.send(f"📡 Broadcast: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("❌ 연결 종료됨")
    finally:
        connected_clients.remove(websocket)

# ✅ Health Check (Render ping 방어용)
async def healthcheck(request):
    return web.Response(text="✅ Server OK - Render Healthcheck Passed")

# ✅ 메인 진입점
async def main():
    import os
    port = int(os.getenv("PORT", 10000))  # Render가 환경변수로 포트 지정함

    # WebSocket 서버
    ws_server = await websockets.serve(ws_handler, "0.0.0.0", port)
    print(f"🚀 WebSocket 서버 시작: ws://0.0.0.0:{port}")

    # HTTP 서버 (Render health check용)
    app = web.Application()
    app.router.add_get("/", healthcheck)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 HTTP 헬스체크 서버 실행 중: http://0.0.0.0:{port}")

    await asyncio.Future()  # 서버 계속 실행 유지

if __name__ == "__main__":
    asyncio.run(main())
