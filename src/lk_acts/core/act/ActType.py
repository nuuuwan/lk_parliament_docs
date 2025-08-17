from dataclasses import dataclass


@dataclass
class ActType:
    name: str
    emoji: str
    color: str

    def is_match(self, description):
        return self.name.lower() in description.lower()

    def as_id(self):
        return self.name.lower().replace(" ", "-")

    @staticmethod
    def list_all():
        return ActType.list_all_except_general() + [ActType.GENERAL]

    @staticmethod
    def list_all_except_general():
        return [
            ActType.AMENDMENT_TO_CONSTITUTION,
            ActType.REPEAL,
            ActType.AMENDMENT,
            ActType.SPECIAL_PROVISION,
            ActType.APPROPRIATION,
            ActType.INCORPORATION,
        ]

    @staticmethod
    def from_description(description):
        for act_type in ActType.list_all_except_general():
            if act_type.is_match(description):
                return act_type
        return ActType.GENERAL

    @staticmethod
    def from_name(name):
        for act_type in ActType.list_all_except_general():
            if act_type.name == name:
                return act_type
        if name == ActType.GENERAL.name:
            return ActType.GENERAL
        raise ValueError(f'Unknown ActType: "{name}"')


ActType.AMENDMENT_TO_CONSTITUTION = ActType(
    name="Amendment to the Constitution", emoji="🔴", color="red"
)

ActType.REPEAL = ActType(name="Repeal", emoji="🟠", color="orange")

ActType.AMENDMENT = ActType(name="Amendment", emoji="🟢", color="green")

ActType.SPECIAL_PROVISION = ActType(
    name="Special Provision", emoji="🔵", color="blue"
)
ActType.APPROPRIATION = ActType(
    name="Appropriation", emoji="🟣", color="purple"
)

ActType.INCORPORATION = ActType(
    name="Incorporation",
    emoji="🟤",
    color="brown",
)
ActType.GENERAL = ActType(name="General", emoji="⚪", color="gray")
