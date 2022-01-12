CURRENT_GROUP = -1

document.addEventListener('DOMContentLoaded', function () {
  const chat_messages = document.querySelector('#messages')
  let first_group_id = null
  if (document.querySelector('#groups') != null) {
    first_group_id = document.querySelector('#groups').firstElementChild.dataset.id
    renderData(first_group_id)
  }

  document.querySelectorAll('.group-item').forEach(function (gi) {
    gi.onclick = function () {
      group_id = gi.dataset.id;
      chat_messages.innerHTML = ''

      renderData(group_id)
    }
  })
  if (document.querySelector('#send-message') != null) {
    document.querySelector('#send-message').onclick = function () {
      const input = document.querySelector('input.form-control')
      const value = input.value
      if (value === '') {
        return
      }
      let user_id = document.querySelector('#send-message').dataset.user_id

      fetch('/user/' + user_id)
        .then(response => response.json())
        .then(user => {

          let tmp = `<div class="message">
                 <img src="` + user['image_url'] + `" alt="user image">
                 <a href="/profile/` + user['id'] + `">` + user['name'] + `</a>
                 <p class="text-muted">` + formatAMPM(new Date()) + `</p>
                 <p>` + value + `</p>
           </div>`

          chat_messages.innerHTML = tmp + chat_messages.innerHTML

          fetch('/add_message/', {
            method: 'POST',
            body: JSON.stringify({
              msg: value,
              user_id: user.id,
              group_id: CURRENT_GROUP,
            })
          }).then(response => response.json())
            .then(response => {
              console.log(response)
            });
        });
      input.value = ''

    }
  }
});

function renderData(group_id) {
  CURRENT_GROUP = group_id
  fetch('/messages/' + group_id)
    .then(response => response.json())
    .then(messages => {
      let tmp = ''
      for (let m in messages) {
        tmp += `
             <div class="message">
                 <img src="` + messages[m].custom_user_image_url + `" alt="user image">
                 <a href="/profile/` + messages[m].custom_user_id + `">` + messages[m].custom_user + `</a>
                 <p class="text-muted">` + formatAMPM(new Date(messages[m].date)) + `</p>
                 <p>` + messages[m].message + `</p>
             </div>`
      }
      document.querySelector('#messages').innerHTML = tmp

    });
}

const formatAMPM = (date) => {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  const ampm = hours >= 12 ? 'pm' : 'am';

  hours %= 12;
  hours = hours || 12;
  minutes = minutes < 10 ? `0${minutes}` : minutes;

  const strTime = `${hours}:${minutes} ${ampm}`;

  return strTime;
};

setInterval(function () {
  if (CURRENT_GROUP !== -1) {
    renderData(CURRENT_GROUP)
  }
}, 5000);