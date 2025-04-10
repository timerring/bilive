---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "bilive"
  text: "Official documentation"
  tagline: 7 x 24 hours unattended recording, rendering danmaku, recognizing subtitles, automatic slicing, automatic uploading, compatible with low-configuration machines, start the project, then everyone can be a recorder.
  actions:
    - theme: brand
      text: Start now
      link: /getting-started
    - theme: alt
      text: View on GitHub
      link: https://github.com/timerring/bilive

features:
  - title: Fast
    details: Using pipeline to process videos, the recording and live broadcast difference is half an hour, and the recording can be uploaded before the broadcast ends!
  - title: Small Occupancy
    details: Simultaneously record multiple live broadcasts and danmaku (including normal danmaku, paid danmaku, and gift ship information), and run in a small space.
  - title: Template
    details: No complex configuration, ready to use, (🎉NEW) automatically fetch related popular tags through the bilibili search suggestion interface.
  - title: (🎉NEW) Automatic slicing upload
    details: Calculate the bullet density to find high-energy fragments and slice them, combine the multi-modal video understanding model GLM-4V-PLUS to automatically generate interesting slice titles and content, and upload them.
  - title: Multi-mode
    details: In addition to the pipeline mode, it also supports append and merge modes, and can automatically detect and merge video streams that are segmented due to network issues or live connection issues.
  - title: Fine-tune rendering danmaku
    details: Automatically convert xml to ass danmaku file and render it to the video to form a video with danmaku, and upload it automatically. There are fine-tune rendering parameters for different video resolutions.
  - title: Low hardware requirements
    details: Even without a GPU, you can complete the recording, danmaku rendering, and uploading process with the most basic single-core CPU and the lowest memory, and there is no minimum configuration requirement. 10-year-old computers or servers can still be used!
  - title: (🎉NEW) Automatic rendering subtitles (requires Nvidia GPU)
    details: Use the open-source model whisper from OpenAI to automatically recognize the audio in the video and convert it to subtitles and render it to the video.
---

