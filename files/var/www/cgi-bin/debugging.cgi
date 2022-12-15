#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="coredump"
plugin_name="Majestic debugging"
page_title="Majestic отладка"
params="consent enabled ftphost ftppath ftppass ftpuser localpath save4web send2devs send2ftp send2tftp tftphost"

[ ! -f "/rom/${mj_bin_file}" ] && redirect_to "status.cgi" "danger" "Majestic не поддерживается на этой системе."

tmp_file=/tmp/${plugin}.conf
config_file=/etc/${plugin}.conf
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Normalization
  # FIXME: strip trailing slashes
  #sanitize "coredump_localpath"
  #sanitize "coredump_ftppath"

  ### Validation
  if [ "true" = "$coredump_enabled" ]; then
    if [ "true" = "$coredump_send2devs" ]; then
      [ -z "$admin_name" ] || [ -z "$admin_email" ] &&
        flash_append "danger" "Пожалуйста, <a href=\"admin.cgi\">заполните профиль админа</a>." && error=1
    fi
    [ "true" != "$coredump_consent"  ] &&
      flash_append "danger" "Вы понимаете и принимаете риски безопасности." && error=1
    [ "true" = "$coredump_send2ftp"  ] && [ -z "$coredump_ftphost"   ] &&
      flash_append "danger" "FTP адрес не может быть пустым." && error=1
    [ "true" = "$coredump_send2tftp" ] && [ -z "$coredump_tftphost"  ] &&
      flash_append "danger" "TFTP адрес не может быть пустым." && error=1
    [ "true" = "$coredump_save4web"  ] && [ -z "$coredump_localpath" ] &&
      flash_append "danger" "Локальный путь не может быть пустым." && error=1
  fi

  if [ -z "$error" ]; then
    # create temp config file
    :>$tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >>$tmp_file
    done; unset _p
    mv $tmp_file $config_file

    update_caminfo
    touch /tmp/coredump-restart.txt
    redirect_back "success" "Конфигурация ${plugin_name} обновлена."
  fi
else
  include $config_file
fi

[ -z "$coredump_ftpuser" ] && coredump_ftpuser="anonymous"
[ -z "$coredump_ftppass" ] && coredump_ftppass="anonymous"
[ -z "$coredump_tftphost" ] && coredump_tftphost=$(fw_printenv -n serverip)

if [ -z "$coredump_localpath" ]; then
  if [ -d "/mnt/mmc" ]; then
    coredump_localpath="/mnt/mmc"
  else
    coredump_localpath="/root"
  fi
fi
%>
<%in p/header.cgi %>

<% if [ -z "$(grep coredump_enabled /etc/init.d/S95*)" ]; then %>
  <div class="alert alert-warning">
    <p><b>Этому сервису требуется небольшая модификация /etc/init.d/S95... файла.</b></p>
    <p>Пожалуйста, вставьте или измените следующий код в функции <code>load_majestic()</code>, прямо перед строкой <code>start-stop-daemon</code>:</p>
    <pre class="bg-light p-3 text-black">
[ -f /etc/coredump.conf ] && . /etc/coredump.conf
if [ "$coredump_enabled" ]; then
  [ "$(yaml-cli -i /etc/majestic.yaml -g .watchdog.timeout)" -lt "30" ] && yaml-cli -i /etc/majestic.yaml -s .watchdog.timeout 30
  ulimit -c unlimited && echo "|/usr/sbin/sendcoredump.sh" >/proc/sys/kernel/core_pattern
fi
</pre>
  </div>
<% fi %>

<% if [ "true" = "$(yaml-cli -g .watchdog.enabled)" ] && [ "$(yaml-cli -g .watchdog.timeout)" -le 60 ]; then %>
<div class="alert alert-warning">
<p class="mb-0">Пожалуйста, отключите watchdog или <a href="majestic-settings.cgi?tab=watchdog">измените значение его тайм-аута</a> на 60 секунд или больше.
Меньший тайм-аут может повлиять на сохранение дампа ядра.</p>
</div>
<% fi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
    <div class="col">
      <h3>Сохранение дампа ядра</h3>
      <% field_switch "coredump_enabled" "Включить сохранение дампа ядра" %>
      <% field_switch "coredump_send2devs" "Отправить дамп ядра разработчикам" %>
      <% field_checkbox "coredump_consent" "Я знаю о возможном наличии конфиденциальной информации в дампах ядра, но доверяю разработчикам" %>

      <button type="button" class="btn btn-info my-3" data-bs-toggle="modal" data-bs-target="#helpModal">Как это работает?</button>
    </div>
    <div class="col">
      <h3>Сохранение на камере</h3>
      <% field_switch "coredump_save4web" "Включить сохранение на камере" "Не рекомендуется сохранять не на SD карту!" %>
      <% field_text "coredump_localpath" "Сохранять в локальную директорию" %>
<% if [ -f "${coredump_localpath}/coredump.tgz" ]; then %>
      <div class="alert alert-danger">
        <h5>На камере уже есть сохраненный дамп ядра!</h5>
        <p class="mb-0">Пожалуйста, скачайте его и удалите /root/coredump.tgz с камеры.</h5>
      </div>
<% fi %>
      <h3>Загрузка на TFTP сервер</h3>
      <% field_switch "coredump_send2tftp" "Включить загрузку на TFTP сервер" %>
      <% field_text "coredump_tftphost" "Хост TFTP сервера" "FQDN или IP адрес" %>
    </div>
    <div class="col">
      <h3>Загрузка на FTP сервер</h3>
      <% field_switch "coredump_send2ftp" "Включить загрузку на FTP сервер" %>
      <% field_text "coredump_ftphost" "Хост FTP сервера" "FQDN или IP адрес" %>
      <% field_text "coredump_ftppath" "Сохранять в FTP директорию" "относительую к корневой FTP директории" %>
      <% field_text "coredump_ftpuser" "Логин" %>
      <% field_password "coredump_ftppass" "Пароль" %>
    </div>
    <div class="col">
      <h3>Конфигурация</h3>
      <% [ -f "$config_file" ] && ex "cat $config_file" %>
    </div>
    <div class="col">
      <h3>Логи последнего сохранения дампа ядра</h3>
      <% [ -f /root/coredump.log ] && ex "cat /root/coredump.log" %>
    </div>
  </div>
  <% button_submit %>
</form>

<div class="modal fade" id="helpModal" tabindex="-1" aria-labelledby="helpModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Как это работает</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <p>Дамп ядра - это содержимое оперативной памяти камеры на момент аварийного завершения работы программы. Дамп ядра используется для последующей отладки программы. Файл с содержимым памяти архивируется вместе с информацией о системе и вашими контактными данными и отправляется на удаленный сервер разработчиков.</p>
        <p>Помните, что дампы ядра могут содержать конфиденциальную информацию, такую как пароли и ключи безопасности. Если вы не желаете, чтобы разработчики получали доступ к таким данным, пожалуйста, не включайте сохранение дампа ядра.</p>
        <p>Если ваша камера имеет не имеет прямого доступа в интернет, вы можете настроить отправку архива на сервер FTP или TFTP в вашей локальной сети, откуда вы сможете переслать файл разработчикам позже вручную. Убедитесь, что сервер FTP/TFTP умеет принимать входящие файлы.</p>
        <p class="mb-0">Если в вашей локальной сети нет сервера FTP/TFTP, чтобы выгрузить на него дамп ядра, вы можете настроить сохранение архива непосредственно на камере. Настоятельно не рекомендуем вам делать этого, если возможен любой другой из вышеописанных вариантов. Сохранение файла на камере может привести к исчерпанию свободного места и нестабильной работе камеры, либо вовсе сделает ее неработоспособной.</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
      </div>
    </div>
  </div>
</div>

<%in p/footer.cgi %>
