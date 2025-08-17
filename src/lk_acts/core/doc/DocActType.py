from dataclasses import dataclass


@dataclass
class DocActType:
    name: str
    emoji: str
    color: str

    def is_match(self, description):
        return self.name.lower() in description.lower()

    def as_id(self):
        return self.name.lower().replace(" ", "-")

    @staticmethod
    def list_all():
        return DocActType.list_all_except_general() + [DocActType.GENERAL]

    @staticmethod
    def list_all_except_general():
        return [
            DocActType.AMENDMENT_TO_CONSTITUTION,
            DocActType.REPEAL,
            DocActType.AMENDMENT,
            DocActType.SPECIAL_PROVISION,
            DocActType.APPROPRIATION,
            DocActType.INCORPORATION,
        ]

    @staticmethod
    def from_description(description):
        for doc_act_type in DocActType.list_all_except_general():
            if doc_act_type.is_match(description):
                return doc_act_type
        return DocActType.GENERAL

    @staticmethod
    def from_name(name):
        for doc_act_type in DocActType.list_all_except_general():
            if doc_act_type.name == name:
                return doc_act_type
        if name == DocActType.GENERAL.name:
            return DocActType.GENERAL
        raise ValueError(f'Unknown DocActType: "{name}"')


DocActType.AMENDMENT_TO_CONSTITUTION = DocActType(
    name="Amendment to the Constitution", emoji="🔴", color="red"
)

DocActType.REPEAL = DocActType(name="Repeal", emoji="🟠", color="orange")

DocActType.AMENDMENT = DocActType(name="Amendment", emoji="🟢", color="green")

DocActType.SPECIAL_PROVISION = DocActType(
    name="Special Provision", emoji="🔵", color="blue"
)
DocActType.APPROPRIATION = DocActType(
    name="Appropriation", emoji="🟣", color="purple"
)

DocActType.INCORPORATION = DocActType(
    name="Incorporation",
    emoji="🟤",
    color="brown",
)
DocActType.GENERAL = DocActType(name="General", emoji="⚪", color="gray")
