# upload common issues

> If you don't find the problem you encountered, please submit it in [issues](https://github.com/timerring/bilive/issues/new/choose).

## Upload default parameters

Customize the relevant configuration in `bilive.toml`, map the keywords to `{artist}`、`{date}`、`{title}`、`{source_link}`, please customize the template by combining and deleting:

- `title` title template.
- `description` description template.
- `gift_price_filter = 1` means filtering gifts with a price lower than 1 yuan.
- `reserve_for_fixing = false` means if the video is uploaded with an error, it will not be reserved for fixing, it is recommended to set false for users with limited hard disk space.
- `upload_line = "auto"` means automatically detecting the upload line and uploading, if you need to specify a fixed line, you can set it to `bldsa`、`ws`、`tx`、`qn`、`bda2`.

## Overly frequent upload

```
Error: ResponseData { code: 137022, data: None, message: "投稿过于频繁，请稍后再试", ttl: Some(1) }
```
```
2024-12-14 20:48:27
2024-12-14 21:19:23
2024-12-14 21:47:27
2024-12-14 22:03:58
2024-12-14 22:21:51
2024-12-14 22:31:35
2024-12-14 22:42:30
2024-12-14 22:51:35
2024-12-14 22:57:21
2024-12-14 23:08:06
2024-12-14 23:16:16
2024-12-14 23:22:33
2024-12-14 23:32:51
2024-12-14 23:40:56
2024-12-14 23:51:25
2024-12-15 00:10:02 Error
```
This error often occurs when uploading frequently in a short period of time, so I personally recommend that the minimum segment should not be less than half an hour, otherwise it will trigger this error. At the same time, if there is a situation where multiple hosts are recorded, it is recommended to adjust the segment interval of the host with lower weight to a larger value, and try to reduce the upload frequency, while setting a shorter interval for the host with higher weight.

Solution: Find the official customer service to lift the account upload restriction within a short period of time.