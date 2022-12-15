#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="SSH ключ"

function readKey() {
  [ -n "$(fw_printenv -n key_${1})" ] && alert "$(fw_printenv -n key_${1})" "secondary" "style=\"overflow-wrap: anywhere;\""
}

function saveKey() {
  if [ -n "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} ключ уже в бэкапе. Вам нужно удалить его, прежде чем сохранить новый ключ."
  else
    fw_setenv key_${1} $(dropbearconvert dropbear openssh /etc/dropbear/dropbear_${1}_host_key - 2>/dev/null | base64 | tr -d '\n')
  fi
}

function restoreKey() {
  if [ -z "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} ключ не в переменных среды."
  else
    fw_printenv -n key_${1} | base64 -d | dropbearconvert openssh dropbear - /etc/dropbear/dropbear_${1}_host_key
    flash_save "success" "${1} ключ восстановлен из переменных среды."
  fi
}

function deleteKey() {
  if [ -z "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} Не удалось найти сохраненный SSH ключ."
  else
    fw_setenv key_${1}
    flash_save "success" "${1} ключ удален из переменных среды."
  fi
}

case "$POST_action" in
  backup)
    saveKey "ed25519"
    redirect_back
    ;;
  restore)
    restoreKey "ed25519"
    redirect_back
    ;;
  delete)
    deleteKey "ed25519"
    redirect_back
    ;;
  *)
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Бэкап ключа</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "backup" %>
      <p>Вы можете сделать бэкап существующего SSH ключа в среду прошивки и восстановить позже, после очистки оверлея.</p>
      <% button_submit "Бэкап SSH ключа" "danger" %>
    </form>
  </div>
  <div class="col">
    <h3>Восстановление ключа</h3>
    <p>Восстановление SSH ключа ранее сохраненного в среде прошивки позволит сохранить аутентификацию существующего клиента.</p>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "restore" %>
      <% button_submit "Восстановить SSH ключ из бэкапа" "danger" %>
    </form>
  </div>
  <div class="col">
    <h3>Удаление ключа</h3>
    <p>Вы можете удалить ключ сохраненный в среде прошивки, а затем, например, заменить его новым.</p>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "delete" %>
      <% button_submit "Удалить SSH ключ." "danger" %>
    </form>
  </div>
</div>

<% readKey "ed25519" %>

<%in p/footer.cgi %>
<% esac %>
