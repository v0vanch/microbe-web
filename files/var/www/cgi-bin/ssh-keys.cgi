#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="$t_sshkey_0"

function readKey() {
  [ -n "$(fw_printenv key_${1})" ] && alert "$(fw_printenv key_${1})" "secondary" "style=\"overflow-wrap: anywhere;\""
}

function saveKey() {
  if [ -n "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} $t_sshkey_a"
  else
    fw_setenv key_${1} $(dropbearconvert dropbear openssh /etc/dropbear/dropbear_${1}_host_key - 2>/dev/null | base64 | tr -d '\n')
  fi
}

function restoreKey() {
  if [ -z "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} $t_sshkey_b"
  else
    fw_printenv key_${1} | sed s/^key_${1}=// | base64 -d | dropbearconvert openssh dropbear - /etc/dropbear/dropbear_${1}_host_key
    flash_save "success" "${1} $t_sshkey_c"
  fi
}

function deleteKey() {
  if [ -z "$(fw_printenv key_${1})" ]; then
    flash_save "danger" "${1} $t_sshkey_d"
  else
    fw_setenv key_${1}
    flash_save "success" "${1} $t_sshkey_e"
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

<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4">
  <div class="col">
    <h3><%= $t_sshkey_1 %></h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "backup" %>
      <p><%= $t_sshkey_2 %></p>
      <% button_submit "$t_sshkey_3" "danger" %>
    </form>
  </div>
  <div class="col">
    <h3><%= $t_sshkey_4 %></h3>
    <p><%= $t_sshkey_5 %></p>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "restore" %>
      <% button_submit "$t_sshkey_6" "danger" %>
    </form>
  </div>
  <div class="col">
    <h3><%= $t_sshkey_7 %></h3>
    <p><%= $t_sshkey_8 %></p>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "delete" %>
      <% button_submit "$t_sshkey_9" "danger" %>
    </form>
  </div>
</div>

<% readKey "ed25519" %>

<%in p/footer.cgi %>
<% esac %>
