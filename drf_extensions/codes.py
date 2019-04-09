ERROR_CODES = {
    # global
    "common": 1000,

    # account
    "authorization": 1001,                  # 账号密码错误
    "authentication_failed": 1002,          # 认证失败
    "user_exist": 1003,                     # 用户已存在
    "user_not_exist": 1004,                 # 用户不存在
    "invalid_code": 1005,                   # 验证码错误
    "sms_send_failed": 1006,                # 短信发送失败
    "password_invalid": 1007,               # 密码错误
    "user_inactive": 1008,                  # 用户未激活

    # system
    "required": 6001,                       # 有必填字段未填
    "invalid_choice": 6002,                 # 参数值不在可选范围内
    "invalid": 6003,                        # 参数错误
    "max_file_size": 6004,                  # 上传文件过大
    "parse_error": 6005,
    "permission_denied": 6403,
    "not_found": 6404,
    "method_not_allowed": 6405,
    "throttled": 6429,
    "internal_server_error": 6500
}
