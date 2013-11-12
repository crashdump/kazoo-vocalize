kazoo-vocalize
==============

Description
-----------

This is Experimental: Don't use in production environment. You've been warned!


Dependencies
------------

 - argparse: https://pypi.python.org/pypi/argparse
 - azoo-api: https://pypi.python.org/pypi/kazoo-api

Commands
--------

```
ref
 [x] are implemented
 [ ] the dude still has some work to do on them
```

 - [x] activate_phone_number        (account_id, phone_number, data)
 - [ ] add_port_in_number           (account_id, phone_number, data)
 - [x] create_callflow              (account_id, data)
 - [ ] create_conference            (account_id, data)
 - [ ] create_deployment            (account_id, server_id, data)
 - [ ] create_device                (account_id, data)
 - [ ] create_directory             (account_id, data)
 - [ ] create_global_resource       (account_id, data)
 - [ ] create_local_resource        (account_id, data)
 - [ ] create_media                 (account_id, data)
 - [ ] create_menu                  (account_id, data)
 - [ ] create_phone_number          (account_id, phone_number)
 - [ ] create_queue                 (account_id, data)
 - [ ] create_temporal_rule         (account_id, data)
 - [ ] create_user                  (account_id, data)
 - [x] create_voicemail_box         (account_id, data)
 - [x] delete_callflow              (account_id, callflow_id)
 - [ ] delete_conference            (account_id, conference_id)
 - [x] delete_device                (account_id, device_id)
 - [ ] delete_directory             (account_id, directory_id)
 - [ ] delete_global_resource       (account_id, resource_id)
 - [ ] delete_local_resource        (account_id, resource_id)
 - [ ] delete_media                 (account_id, media_id)
 - [ ] delete_menu                  (account_id, menu_id)
 - [ ] delete_phone_number          (account_id, phone_number)
 - [ ] delete_phone_number_doc      (account_id, phone_number, filename)
 - [x] delete_queue                 (account_id, queue_id)
 - [ ] delete_temporal_rule         (account_id, rule_id)
 - [x] delete_user                  (account_id, user_id)
 - [ ] delete_voicemail_box         (account_id, vmbox_id)
 - [x] get_account                  (account_id)
 - [x] get_account_children         (account_id)
 - [x] get_account_descendants      (account_id)
 - [x] get_all_devices_status       (account_id)
 - [x] get_all_media                (account_id)
 - [x] get_callflow                 (account_id, callflow_id)
 - [x] get_callflows                (account_id)
 - [ ] get_conference               (account_id, conference_id)
 - [ ] get_conferences              (account_id)
 - [ ] get_deployment               (account_id, server_id)
 - [x] get_device                   (account_id, device_id)
 - [x] get_devices                  (account_id)
 - [ ] get_directories              (account_id)
 - [ ] get_directory                (account_id, directory_id)
 - [ ] get_global_resource          (account_id, resource_id)
 - [ ] get_global_resources         (account_id)
 - [ ] get_hotdesk                  (account_id)
 - [ ] get_limits                   (account_id)
 - [ ] get_local_resource           (account_id, resource_id)
 - [ ] get_local_resources          (account_id)
 - [ ] get_media                    (account_id, media_id)
 - [ ] get_menu                     (account_id, menu_id)
 - [ ] get_menus                    (account_id)
 - [ ] get_phone_numbers            (account_id)
 - [x] get_queue                    (account_id, queue_id)
 - [x] get_queues                   (account_id)
 - [x] get_server_log               (account_id)
 - [x] get_servers                  (account_id)
 - [ ] get_temporal_rule            (account_id, rule_id)
 - [ ] get_temporal_rules           (account_id)
 - [x] get_user                     (account_id, user_id)
 - [x] get_users                    (account_id)
 - [x] get_voicemail_box            (account_id, vmbox_id)
 - [x] get_voicemail_boxes          (account_id)
 - [ ] reserve_phone_number         (account_id, phone_number, data)
 - [ ] search_phone_numbers         (prefix, quantity=10)
 - [ ] update_account               (account_id, data)
 - [ ] update_callflow              (account_id, callflow_id, data)
 - [ ] update_conference            (account_id, conference_id, data)
 - [x] update_device                (account_id, device_id, data)
 - [ ] update_directory             (account_id, directory_id, data)
 - [ ] update_global_resource       (account_id, resource_id, data)
 - [ ] update_local_resource        (account_id, resource_id, data)
 - [ ] update_media                 (account_id, media_id, data)
 - [ ] update_menu                  (account_id, menu_id, data)
 - [ ] update_phone_number          (account_id, phone_number, data)
 - [ ] update_queue                 (account_id, queue_id, data)
 - [ ] update_temporal_rule         (account_id, rule_id, data)
 - [ ] update_user                  (account_id, user_id, data)
 - [ ] update_voicemail_box         (account_id, vmbox_id, data)
 - [ ] upload_phone_number_file     (account_id, phone_number, filename, file_obj)
