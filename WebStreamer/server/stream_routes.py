# Avishkar Patil | AbirHasan2005

import math
import logging
import secrets
import mimetypes
from ..vars import Var
from aiohttp import web
from ..bot import StreamBot
from ..utils.custom_dl import TGCustomYield, chunk_size, offset_fix

routes = web.RouteTableDef()


@routes.get("/", allow_head=True)
async def root_route_handler(request):
    bot_details = await StreamBot.get_me()
    return web.json_response({"status": "running",
                              "maintained_by": "Papkorn Co.",
                              "server_permission": "Do not touch the server",
                              "Telegram_Bot": 'https://t.me/PapkornBot'})


@routes.get("/pk/{message_id}")
@routes.get("/pk/{message_id}/")
@routes.get(r"/pk/{message_id:\d+}/{name}")
async def stream_handler(request):
    try:
        # print('Entered Message ID: {}'.format(request.match_info['message_id']))
        message_id = int(request.match_info['message_id'])
        return await media_streamer(request, message_id)
    except ValueError as e:
        logging.error("Error in stram handler\r")
        logging.error(e)
        raise web.HTTPNotFound


async def media_streamer(request, message_id: int):
    range_header = request.headers.get('Range', 0)
    media_msg = await StreamBot.get_messages(Var.BIN_CHANNEL, message_id)
    # print("media message: {} - [{}]".format(media_msg, Var.BIN_CHANNEL))
    file_properties = await TGCustomYield().generate_file_properties(media_msg)
    # print("File properties: {}".format(file_properties))
    file_size = file_properties.file_size
    # print('File size {}'.format(file_size))

    if range_header:
        from_bytes, until_bytes = range_header.replace('bytes=', '').split('-')
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = request.http_range.stop or file_size - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    req_length = until_bytes - from_bytes + 1

    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
    
    body = TGCustomYield().yield_file(media_msg, offset, first_part_cut, last_part_cut, part_count,
                                      chunk_size)

    file_name = file_properties.file_name if file_properties.file_name \
        else f"{secrets.token_hex(2)}.jpeg"
    print('File name {}'.format(file_name))
    mime_type = file_properties.mime_type if file_properties.mime_type \
        else f"{mimetypes.guess_type(file_name)}"

    return_resp = web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": mime_type,
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'attachment; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        }
    )

    return return_resp
