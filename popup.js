const STORAGE_KEY = 'vsc_speed';

const statusEl = document.getElementById('status');
const buttons = document.querySelectorAll('.speed-btn');

function showStatus(text, type) {
  statusEl.textContent = text;
  statusEl.className = `status ${type}`;
  clearTimeout(statusEl._timer);
  statusEl._timer = setTimeout(() => {
    statusEl.className = 'status hidden';
  }, 2000);
}

function setActiveButton(speed) {
  buttons.forEach(btn => {
    btn.classList.toggle('active', parseFloat(btn.dataset.speed) === speed);
  });
}

async function getCurrentTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

// On popup open: reflect stored speed, then check the actual video
chrome.storage.local.get([STORAGE_KEY], async ({ vsc_speed }) => {
  if (vsc_speed) setActiveButton(vsc_speed);

  try {
    const tab = await getCurrentTab();
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id, allFrames: true },
      func: () => {
        const video = document.querySelector('video');
        return video ? video.playbackRate : null;
      },
    });
    const rate = results.map(r => r.result).find(r => r !== null);
    if (rate) setActiveButton(rate);
  } catch (_) {}
});

// Button click: directly execute speed change in the page (no message passing)
buttons.forEach(btn => {
  btn.addEventListener('click', async () => {
    const speed = parseFloat(btn.dataset.speed);
    const tab = await getCurrentTab();

    let results;
    try {
      results = await chrome.scripting.executeScript({
        target: { tabId: tab.id, allFrames: true },
        func: (s) => {
          const videos = document.querySelectorAll('video');
          videos.forEach(v => { v.playbackRate = s; });
          return videos.length;
        },
        args: [speed],
      });
    } catch (err) {
      showStatus('Cannot access this page.', 'error');
      return;
    }

    const totalVideos = results.reduce((sum, r) => sum + (r.result || 0), 0);

    if (totalVideos === 0) {
      showStatus('No videos found on this page.', 'error');
      return;
    }

    const label = speed === 1 ? 'Normal speed' : `Speed set to ${speed}×`;
    const extra = totalVideos > 1 ? ` (${totalVideos} videos)` : '';
    showStatus(`${label}${extra}`, 'success');
    setActiveButton(speed);
    chrome.storage.local.set({ [STORAGE_KEY]: speed });
  });
});
