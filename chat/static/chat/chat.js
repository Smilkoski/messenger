document.addEventListener('DOMContentLoaded', function () {

  renderData(1)
  document.querySelectorAll('.group-item').forEach(function (gi) {
    gi.onclick = function () {
      console.log(gi.dataset.id);
      group_id = gi.dataset.id;
      const chat = document.querySelector('#chat')
      chat.innerHTML = ''

      renderData(group_id)
    }
  })

});

function renderData(group_id) {
  fetch('/messages/' + group_id)
    .then(response => response.json())
    .then(messages => {
      console.log(messages)
      tmp = ''
      for (m in messages) {
        tmp += `
             <div class="message">
                 <img src="` + messages[m].custom_user_image_url + `" alt="user image">
                 <a href="/profile/` + messages[m].custom_user_id + `">` + messages[m].custom_user + `</a>
                 <p class="text-muted">` + formatAMPM(new Date(messages[m].date)) + `</p>
                 <p>` + messages[m].message + `</p>
             </div>`
      }
      chat.innerHTML = tmp
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