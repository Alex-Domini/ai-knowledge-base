class ParserService:
    async def parse_txt(self, content: bytes) -> str:
        return content.decode("utf-8")
