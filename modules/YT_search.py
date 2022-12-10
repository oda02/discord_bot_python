import json
import aiohttp


class YoutubeSearch:

    @classmethod
    async def search(cls, search_terms: str, max_results: int = None):
        async with aiohttp.ClientSession() as session:
            url = 'https://www.youtube.com/results'
            async with session.get(url, params={'search_query':search_terms}) as resp:
                response = await resp.text()
                results = await cls._parse_html(response)
                if max_results is not None and len(results) > max_results:
                    return results[: max_results]
                return results

    @classmethod
    async def _parse_html(cls, response):
        results = []
        start = (
                response.index("ytInitialData")
                + len("ytInitialData")
                + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        for contents in \
        data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]:
            for video in contents["itemSectionRenderer"]["contents"]:
                res = {}
                if "videoRenderer" in video.keys():
                    video_data = video.get("videoRenderer", {})
                    res["id"] = video_data.get("videoId", None)
                    # res["thumbnails"] = [thumb.get("url", None) for thumb in
                    #                      video_data.get("thumbnail", {}).get("thumbnails", [{}])]
                    res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                    res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text",
                                                                                                         None)
                    res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                    res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                    res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0)
                    res["publish_time"] = video_data.get("publishedTimeText", {}).get("simpleText", 0)

                    res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get(
                        "webCommandMetadata", {}).get("url", None)
                    res["url"] = f'https://www.youtube.com{res["url_suffix"]}'
                    results.append(res)

            if results:
                return results
        return results

