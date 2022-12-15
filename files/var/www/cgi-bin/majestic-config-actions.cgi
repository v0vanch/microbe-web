#!/usr/bin/haserl --upload-limit=20 --upload-dir=/tmp
<%in p/common.cgi %>
<%
config_file=/etc/majestic.yaml
config_file_fw=/rom/etc/majestic.yaml

if [ "POST" = "$REQUEST_METHOD" ]; then
  case "$POST_action" in
    backup)
      echo "HTTP/1.0 200 OK
Date: $(time_http)
Server: $SERVER_SOFTWARE
Content-type: text/plain
Content-Disposition: attachment; filename=majestic.yaml
Content-Length: $(wc -c $config_file | cut -d' ' -f1)
Cache-Control: no-store
Pragma: no-cache
"
      cat $config_file
      ;;
    patch)
      patch_file=/tmp/majestic.patch
      diff $config_file_fw $config_file >$patch_file
      echo "HTTP/1.0 200 OK
Date: $(time_http)
Server: $SERVER_SOFTWARE
Content-type: text/plain
Content-Disposition: attachment; filename=majestic.$(time_epoch).patch
Content-Length: $(wc -c $patch_file | cut -d' ' -f1)
Cache-Control: no-store
Pragma: no-cache
"
      cat $patch_file
      rm $patch_file
      ;;
    reset)
      /usr/sbin/sysreset.sh -m
      redirect_back
      ;;
    restore)
      magicnum="23206d616a6573746963"
      file="$POST_mj_restore_file"
      file_name="$POST_mj_restore_file_name"
      file_path="$POST_mj_restore_file_path"
      error=""
      [ -z "$file_name" ] && error="Файл не найден! Вы не забыли его загрузить?"
      [ ! -r "$file" ] && error="Не получилось прочитать загруженный файл!"
      [ "$(wc -c "$file" | awk '{print $1}')" -gt "$maxsize" ] && error="Загруженный файл слишком большой! $(wc -c $file | awk '{print $1}') > ${maxsize}."
      #[ "$magicnum" -ne "$(xxd -p -l 10 $file)" ] && error="Магические числа файла не совпадают. Вы загружаете корректный файл? $(xxd -p -l 10 $file) != $magicnum"
      if [ -z "$error" ]; then
        # yaml-cli -i $POST_upfile -o /tmp/majestic.yaml # FIXME: sanitize
        mv $file_path /etc/majestic.yaml
        redirect_to $SCRIPT_NAME
      fi
      ;;
  esac
fi
%>

<% page_title="Обслуживание Majestic" %>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Бэкап конфигурации</h3>
    <p>Скачайте файл majestic.yaml, чтобы сохранить изменения в конфигурации Majestic.</p>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "backup" %>
      <% button_submit "Скачать конфигурацию" %>
    </form>
  </div>
  <div class="col">
    <h3>Восстановление конфигурации</h3>
    <p>Восстановите конфигурацию Majestic из скачанного ранее файла majestic.yaml.</p>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <% field_hidden "action" "restore" %>
      <% field_file "mj_restore_file" "Файл бэкапа" "majestic.yaml" %>
      <% button_submit "Загрузить конфигурацию" "warning" %>
    </form>
  </div>
  <div class="col">
    <h3>Просмотр отличий</h3>
    <p>Сравните текущий файл majestic.yaml с тем, что поставляется с прошивкой.</p>
    <a class="btn btn-primary" href="majestic-config-compare.cgi">Просмотреть отличия</a>
  </div>
  <div class="col">
    <h3>Экспортировать как патч</h3>
    <p>Экспортируйте измнения в файле majestic.yaml в форме файла патча.</p>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_hidden "action" "patch" %>
      <% button_submit "Скачать патч" %>
    </form>
  </div>
  <div class="col">
    <h3>Сброс</h3>
    <% if [ "$(diff -q $config_file_fw $config_file)" ]; then %>
      <p>Сбросьте изменения конфигурации Majestic в исходное состояние.</p>
      <% button_mj_reset %>
    <% else %>
      <p>Нет изменений для сброса! Конфигурация Majestic не отличается от исходного состояния.</p>
    <% fi %>
  </div>
</div>

<%in p/footer.cgi %>
