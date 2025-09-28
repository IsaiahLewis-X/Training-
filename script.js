const messagesContainer = document.querySelector('#messages');
const form = document.querySelector('#chat-form');
const input = document.querySelector('#user-input');
const template = document.querySelector('#message-template');

const assistantName = 'Lumi';

const promptLibrary = [
  {
    keywords: ['hello', 'hi', 'hey', 'greetings'],
    responses: [
      "Hey there! It's great to meet you. How can I help today?",
      "Hello! I'm here and ready to dive into anything you're curious about.",
      "Hi! What would you like to chat about first?"
    ]
  },
  {
    keywords: ['help', 'support', 'assist'],
    responses: [
      "I can brainstorm ideas, offer productivity tips, or simply keep you company while you work.",
      "Need a second brain? I can help plan tasks, explain tricky topics, or come up with creative prompts.",
      "I'm a flexible assistant—ask about focus routines, healthy breaks, or even fun trivia!"
    ]
  },
  {
    keywords: ['productivity', 'focus', 'motivation'],
    responses: [
      "Try a 25-minute focus sprint followed by a 5-minute stretch. It keeps your mind energized!",
      "Setting a tiny, achievable goal for the next 10 minutes is a wonderful motivation kickstarter.",
      "Pair tasks with music that matches your pace—lo-fi for deep focus, upbeat tunes for energy."
    ]
  },
  {
    keywords: ['break', 'bored', 'relax'],
    responses: [
      "How about a quick window stretch? Let your eyes rest on something 20 feet away for 20 seconds.",
      "Grab a glass of water and take five mindful breaths—tiny reset, big difference!",
      "Maybe doodle your favorite animal for 2 minutes; playful creativity can reset your brain."
    ]
  },
  {
    keywords: ['thank', 'thanks', 'appreciate'],
    responses: [
      "Anytime! Helping you out is my favorite thing.",
      "You're welcome! Let me know if there's anything else you'd like to explore.",
      "Happy to be here for you—just say the word if you need more support."
    ]
  }
];

const fallbackResponses = [
  "That's interesting! Tell me more so I can come up with a helpful suggestion.",
  "I might not have the perfect answer yet, but I'm eager to figure it out with you.",
  "Let's explore that together—what part should we tackle first?"
];

function createMessageElement({ sender, text, isUser = false }) {
  const fragment = template.content.cloneNode(true);
  const messageEl = fragment.querySelector('.message');
  const senderEl = fragment.querySelector('.sender');
  const textEl = fragment.querySelector('.text');
  const timeEl = fragment.querySelector('time');
  const avatarEl = fragment.querySelector('.avatar');

  messageEl.classList.toggle('user', isUser);
  senderEl.textContent = sender;
  textEl.textContent = text;
  timeEl.textContent = new Intl.DateTimeFormat('en', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true
  }).format(new Date());

  avatarEl.textContent = sender
    .split(' ')
    .map((word) => word[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();

  return fragment;
}

function appendMessage(options) {
  const messageFragment = createMessageElement(options);
  messagesContainer.appendChild(messageFragment);
  messagesContainer.scrollTo({
    top: messagesContainer.scrollHeight,
    behavior: 'smooth'
  });
}

function getAssistantResponse(userText) {
  const normalized = userText.toLowerCase();

  for (const prompt of promptLibrary) {
    if (prompt.keywords.some((keyword) => normalized.includes(keyword))) {
      return randomItem(prompt.responses);
    }
  }

  return randomItem(fallbackResponses);
}

function randomItem(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function simulateAssistantThinking(callback) {
  const thinkingText = '…thinking';
  const thinkingId = `thinking-${crypto.randomUUID()}`;

  appendMessage({ sender: assistantName, text: thinkingText });

  const placeholder = messagesContainer.lastElementChild;
  placeholder.dataset.thinkingId = thinkingId;

  const delay = Math.random() * 800 + 400;

  setTimeout(() => {
    const finalResponse = callback();
    if (!finalResponse) return;

    const bubble = placeholder.querySelector('.text');
    bubble.textContent = finalResponse;
  }, delay);
}

function sendUserMessage(text) {
  appendMessage({ sender: 'You', text, isUser: true });

  simulateAssistantThinking(() => getAssistantResponse(text));
}

function seedConversation() {
  appendMessage({
    sender: assistantName,
    text: "Hello! I'm Lumi, your friendly AI assistant. What would you like to explore together today?"
  });
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  sendUserMessage(text);
  form.reset();
  input.focus();
});

seedConversation();
