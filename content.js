// Listen for speed change messages from the popup
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.action === 'setSpeed') {
    const videos = document.querySelectorAll('video');
    if (videos.length === 0) {
      sendResponse({ success: false, message: 'No videos found on this page' });
      return true;
    }
    videos.forEach(video => {
      video.playbackRate = message.speed;
    });
    sendResponse({ success: true, count: videos.length, speed: message.speed });
    return true;
  }

  if (message.action === 'getSpeed') {
    const video = document.querySelector('video');
    if (!video) {
      sendResponse({ success: false, speed: 1 });
      return true;
    }
    sendResponse({ success: true, speed: video.playbackRate });
    return true;
  }

  return true;
});
