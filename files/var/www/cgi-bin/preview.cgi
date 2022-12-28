#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Камера"

size=$(yaml-cli -g .mjpeg.size); [ -z "$size" ] && size="640x480"
size_w=${size%x*}
size_h=${size#*x}
%>
<%in p/header.cgi %>

<div class="row preview">
  <div class="col-md-8 col-xl-9 col-xxl-9 position-relative mb-3">
    <% preview 1 %>
  </div>
  <div class="col-md-4 col-xl-3 col-xxl-3">
    <div class="d-grid gap-2 mb-3">
      <div class="input-group">
        <div class="input-group-text">
          <img src="/a/light-off.svg" alt="Image: Night mode indicator" id="night-mode-status">
        </div>
        <button class="form-control btn btn-primary text-start" type="button" id="toggle-night-mode">Вкл/выкл ночной режим</button>
        <%#
        <div class="input-group-text">
          <a href="majestic-settings.cgi?tab=nightMode" title="Night mode settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
        %>
      </div>
      <%#
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="email">Отправить по email</button>
        <div class="input-group-text">
          <a href="plugin-send2email.cgi" title="Email settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="ftp">Отправить по FTP</button>
        <div class="input-group-text">
          <a href="plugin-send2ftp.cgi" title="FTP Storage settings"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="telegram">Отправить через Telegram</button>
        <div class="input-group-text">
          <a href="plugin-send2telegram.cgi" title="Настройки Telegram бота"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="webhook">Отправить на веб-хук</button>
        <div class="input-group-text">
          <a href="plugin-send2webhook.cgi" title="Настройки веб-хука"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="yadisk">Отправить на Яндекс Диск</button>
        <div class="input-group-text">
          <a href="plugin-send2yadisk.cgi" title="Настройки Яндекс Диска"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      <div class="input-group">
        <button class="form-control btn btn-primary text-start" type="button" data-sendto="openwall">Отправить на Open Wall</button>
        <div class="input-group-text">
          <a href="plugin-send2openwall.cgi" title="Настройки Open Wall"><img src="/a/gear.svg" alt="Gear"></a>
        </div>
      </div>
      %>
    </div>
    <%#
    <div class="alert alert-danger small">
      Функция PTZ еще не готова.
    </div>
    %>
  </div>
</div>

<script>
const network_address = "<%= $network_address %>";

<%# [ "true" != "$email_enabled"    ] && echo "\$('button[data-sendto=email]').disabled = true;" %>
<%# [ "true" != "$ftp_enabled"      ] && echo "\$('button[data-sendto=ftp]').disabled = true;" %>
<%# [ "true" != "$webhook_enabled"  ] && echo "\$('button[data-sendto=webhook]').disabled = true;" %>
<%# [ "true" != "$telegram_enabled" ] && echo "\$('button[data-sendto=telegram]').disabled = true;" %>
<%# [ "true" != "$yadisk_enabled"   ] && echo "\$('button[data-sendto=yadisk]').disabled = true;" %>

function reqListener(data) {
  console.log(data.responseText);
}

function sendToApi(endpoint) {
  const xhr = new XMLHttpRequest();
  xhr.addEventListener("load", reqListener);
  xhr.open("GET", "http://" + network_address + endpoint);
  xhr.setRequestHeader("Authorization", "Basic " + btoa("admin:"));
  xhr.send();
}

$$("a[id^=pan-],a[id^=zoom-]").forEach(el => {
  el.addEventListener("click", event => {
    event.preventDefault();
    alert("Эта функция пока не работает!");
  });
});

$("#toggle-night-mode")?.addEventListener("click", event => {
  event.preventDefault();
  $('#night-mode-status').src = ($('#night-mode-status').src.split("/").pop() == "light-on.svg") ? "/a/light-off.svg" : "/a/light-on.svg";
  // sendToApi("/night/toggle");
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/cgi-bin/night.cgi");
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.send("mode=toggle");
});

$$("button[data-sendto]").forEach(el => el.addEventListener("click", event => {
    event.preventDefault();
    if (!confirm("Are you sure?")) return false;
    const tgt = event.target.dataset["sendto"];
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/cgi-bin/send.cgi?to=" + tgt);
    xhr.send();
}))

$("#speed")?.addEventListener("click", event => {
  event.preventDefault();
  event.target.src = (event.target.src.split("/").pop() == "speed-slow.svg") ? "/a/speed-fast.svg" : "/a/speed-slow.svg";
  // sendToApi("/speed/toggle");
});
</script>

<%in p/footer.cgi %>
