#!/usr/bin/haserl --upload-limit=100 --upload-dir=/tmp
<%in p/common.cgi %>
<%
locale_file=/etc/webui/locale

if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$POST_action" in
  access)
    new_password="$POST_ui_password"
    [ -z "$new_password" ] && error="Пароль не может быть пустым!"
    [ "$ui_password_fw" = "$new_password" ] && error="Нельзя использовать стандартный пароль!"
    [ -n "$(echo "$new_password" | grep " ")" ] && error="Пароль не может содержать пробелы!"
    [ "5" -ge "${#new_password}" ] && error="Пароль не может быть короче 6 символов!"

    [ -n "$error" ] && redirect_to $SCRIPT_NAME "danger" "$error"

    sed -i s/:admin:.*/:admin:${new_password}/ /etc/httpd.conf
    echo "root:${new_password}" | chpasswd
    update_caminfo

    # prepare for passwordless login
    [ ! -d "/root/.ssh" ] && ln -s /etc/dropbear /root/.ssh

    redirect_to "/" "success" "Пароль обновлен."
    ;;

  locale)
    locale="$POST_ui_language" # set language.
    # upload new language and switch to it. overrides aboveset language.
    _fname="$POST_ui_locale_file_name"
    if [ -n "$_fname" ]; then
      mv "$POST_ui_locale_file_path" /var/www/lang/$_fname
      locale=${_fname%%.*}
    fi
    # save new language settings and reload locale
    [ -z "$locale" ] && locale="en"
    echo "$locale" >$locale_file
    reload_locale
    update_caminfo
    redirect_to $SCRIPT_NAME "success" "Язык обновлен."
    ;;

  *)
    redirect_to $SCRIPT_NAME "danger" "UNKNOWN ACTION: $POST_action"
    ;;
  esac
fi

page_title="Настройки веб-интерфейса"

# data for form fields
ui_username="admin"
ui_language="$locale"

ui_locales="en|English"
if [ -d /var/www/lang/ ]; then
 for i in $(ls -1 /var/www/lang/); do
    code="$(basename $i)"; code="${code%%.sh}"
    name="$(sed -n 2p $i|sed "s/ /_/g"|cut -d: -f2)"
    ui_locales="${ui_locales},${code}|${name}"
  done
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Доступ</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "access" %>
      <p class="string">
        <label for="ui_username" class="form-label">Логин</label>
        <input type="text" id="ui_username" name="ui_username" value="admin" class="form-control" autocomplete="username" disabled>
      </p>
      <% field_password "ui_password" "Пароль" %>
      <% button_submit %>
    </form>
  </div>
<!--
  <div class="col">
    <h3>Язык</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <% field_hidden "action" "locale" %>
      <% field_select "ui_language" "Язык интерфейса" "$ui_locales" %>
      <%# field_file "ui_locale_file" "Файл локализации" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <h3>Конфигурация</h3>
    <%
    ex "cat /etc/httpd.conf"
    #ex "echo \$locale"
    #ex "cat $locale_file"
    #ex "ls /var/www/lang/"
    %>
  </div>
-->
</div>

<%in p/footer.cgi %>
