import os
import shutil
import tempfile

from model.rule import Rule as DBRule
from model.profile import Profile as DBProfile


def clean(profiles, rules_buffer):
    rules_buffer.append("iptables -F INPUT")
    for profile in profiles:
        rules_buffer.append("iptables -F {}".format(profile.name))
        rules_buffer.append("iptables -X {}".format(profile.name))


def create_tables(profiles, rules_buffer):
    for profile in profiles:
        rules_buffer.append("iptables -N {}".format(profile.name))
        rules_buffer.append("iptables -I INPUT -j {}".format(profile.name))
        rules_buffer.append("iptables -A administrator -j DROP")


def start_input_rules(rules_buffer):
    rules_buffer.append("iptables -I INPUT -p tcp --dport 80 -j ACCEPT")
    rules_buffer.append(
        "iptables -I INPUT -p tcp -m state --state ESTABLISHED,RELATED -j ACCEPT"
    )


def finish_input_rules(rules_buffer):
    rules_buffer.append("iptables -I INPUT -j DROP")


def apply_to_os(rules_buffer):
    rules_file = tempfile.mkstemp(dir="/tmp")[1]
    with open(rules_file, 'w') as r_f:
        r_f.write("#!/bin/bash\n")
        for rule in rules_buffer:
            r_f.write("{}\n".format(rule))

    os.system("chmod a+x {}".format(rules_file))
    os.system(rules_file)
    shutil.rmtree(rules_file)


def apply_rules(session):
    rules_buffer = list()
    profiles = session.query(DBProfile).all()
    clean(profiles, rules_buffer)
    start_input_rules(rules_buffer)
    create_tables(profiles, rules_buffer)
    profiles_as_dict = dict()
    for profile in profiles:
        profiles_as_dict[profile.id] = profile.name

    for rule in session.query(DBRule).all():
        rules_buffer.append("iptables -I {} {}".format(
            profiles_as_dict[rule.profile_id], rule.as_iptables()
        ))

    finish_input_rules(rules_buffer)
    apply_to_os(rules_buffer)
