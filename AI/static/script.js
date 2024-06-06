$(document).ready(function() {
  // Event listeners for sending messages
  $('#send-button').click(sendMessage);
  $('#user-query').keypress(function(e) {
    if (e.which == 13 && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Function to send user message and handle response
  function sendMessage() {
    var query = $('#user-query').val().trim();

    if (query === '') return;

    addUserMessage(query);
    $('#user-query').val('');

    $.ajax({
      url: '/generate',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ prompt: query }),
      success: function(response) {
        if (response.image_url) {
          addImageMessage(response.image_url);
        } else if (response.response) {
          addAssistantMessage(response.response);
        } else {
          console.error('Unexpected response format:', response);
        }
      },
      error: function(error) {
        console.error('Error:', error);
      }
    });
  }

  // Function to add user message to chat container
  function addUserMessage(message) {
    $('#chat-container').append('<div class="message user-message">' + message.replace(/\n/g, '<br>') + '</div>');
    scrollToBottom();
  }

  // Function to add assistant message to chat container
  function addAssistantMessage(message) {
    $('#chat-container').append('<div class="message assistant-message">' + message.replace(/\n/g, '<br>') + '</div>');
    scrollToBottom();
  }

  // Function to add image message to chat container
  function addImageMessage(imageUrl) {
    $('#chat-container').append('<div class="message assistant-message"><img src="' + imageUrl + '" alt="Generated Image" style="max-width: 100%; height: auto; border-radius: 5px;"></div>');
    scrollToBottom();
  }

  // Function to scroll chat container to the bottom
  function scrollToBottom() {
    $('#chat-container').animate({ scrollTop: $('#chat-container').prop('scrollHeight') }, 300);
  }
});

