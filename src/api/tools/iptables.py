from model.rule import Rule as DBRule
from model.profile import Profile as DBProfile


def create_tables(profiles):
    for profile in profiles:
        print "iptables -N {}".format(profile.name)


def apply_rules(session):
    profiles = session.query(DBProfile).all()
    create_tables(profiles)
    profiles_as_dict = dict()
    for profile in profiles:
        profiles_as_dict[profile.id] = profile.name

    for rule in session.query(DBRule).all():
        print "iptables -A {} {}".format(
            profiles_as_dict[rule.profile_id], rule.as_iptables()
        )
