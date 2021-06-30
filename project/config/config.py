conf={
    "dbconf":{
        "dbname":"mahajan_jewellers_dev",
        "dbuser":"postgres",
        "dbpassword":"123123",
        "dbhost":"localhost",
        "dbport":5432
    },
    "roles_config":{
        # Do not change the Keys !!!
        # You may add new Key-values
        # You may modify values associated with a key
        "admin_only":"admin",
        "reseller":["admin","reseller"],
        "customer":["admin","customer"],
        "all":["admin", "customer", "reseller"]
    }
}