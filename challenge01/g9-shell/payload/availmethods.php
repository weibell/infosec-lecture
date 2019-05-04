<?php

$execMethods = [
    'ReflectionFunction'    => class_exists('ReflectionFunction'),
    'call_user_func'        => function_exists('call_user_func'),
    'call_user_func_array'  => function_exists('call_user_func_array'),
    'exec'                  => function_exists('exec'),
    'fsockopen'             => function_exists('fsockopen'),
    'pcntl_fork'            => function_exists('pcntl_fork'),
    'proc_open'             => function_exists('proc_open'),
    'shell_exec'            => function_exists('shell_exec'),
    'system'                => function_exists('system')
];

print_r($execMethods);
