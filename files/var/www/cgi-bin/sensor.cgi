#!/usr/bin/haserl --upload-limit=200 --upload-dir=/tmp
<%in p/common.cgi %>
<%
page_title="Sensor Driver and Config"

if [ "POST" = "$REQUEST_METHOD" ]; then
  error=""

  if [ -n "$POST_sensor_driver_file" ]; then
    type="driver"
    magicnum="7f454c460101"
    file="$POST_sensor_driver_file"
    file_name="$POST_sensor_driver_file_name"
    file_path="$POST_sensor_driver_file_path"

    if [ -z "$file_name" ]; then
      error="Файл не найден! Вы не забыли его загрузить?"
    elif [ "$magicnum" != $(xxd -p -l 6 $file) ]; then
      error="Магические числа файла не совпадают. Вы загружаете корректный файл?"
    elif [ -f "/usr/lib/sensors/${file_name}" ]; then
      error="Файл уже существует!"
    fi
  fi

  if [ -n "$POST_sensor_config_file" ]; then
    type="config"
    file="$POST_sensor_config_file"
    file_name="$POST_sensor_config_file_name"
    file_path="$POST_sensor_config_file_path"
    if [ -z "$file_name" ]; then
      error="Файл не найден! Вы не забыли его загрузить?"
    elif [ -n $(grep "\[sensor\]" $file) ]; then
      error="Магические числа файла не совпадают. Вы загружаете корректный файл?"
    elif [ -f "/etc/sensors/${file_name}" ]; then
      error="Файл уже существует!"
    fi
  fi

  if [ -z "$error" ]; then
    case "$type" in
    driver)
      mv "$file_path" "/usr/lib/sensors/${file_name}"
      redirect_to $SCRIPT_NAME "success" "Драйвер сенсора загружен."
      ;;
    config)
      mv "$file_path" "/etc/sensors/${file_name}"
      redirect_to $SCRIPT_NAME "success" "Конфигурация сенсора загружена."
      ;;
    esac
  fi
fi
%>
<%in p/header.cgi %>

<% [ -n "$error" ] && report_error "$error" %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Драйвера сенсора</h3>
    <% ex "ls /usr/lib/sensors/" %>
  </div>
  <div class="col">
    <h3>Загрузить драйвер сенсора</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <% field_file "sensor_driver_file" "Файл драйвера сенсора" %>
      <% button_submit "Загрузить файл" %>
    </form>
  </div>
  <div class="col">
    <h3>Конфигурация сенсора</h3>
    <% ex "ls /etc/sensors/" %>
  </div>
  <div class="col">
    <h3>Загрузить конфигурацию сенсора</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <% field_file "sensor_config_file" "Файл конфигурации сенсора" %>
      <% button_submit "Загрузить файл" %>
    </form>
  </div>
</div>

<%in p/footer.cgi %>
