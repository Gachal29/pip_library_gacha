import json
import os, sys
import copy

class SettingRules:
    __debug: bool = False
    __rules: json = None
    __rule_items: list[str] = None

    __BASE_DIR: str = os.path.dirname(__file__)
    __default_rules_file_path = __BASE_DIR + "/DefaultRules/rules.json"
    
    def setting_rules(self, rules_file_path: str = None):
        if self.__debug:
            print("setting_rules")

        setting_mode: str = "custom"
        if not rules_file_path:
            setting_mode = "default"
            rules_file_path = self.__default_rules_file_path

        try:
            with open(rules_file_path, "r", encoding="utf-8-sig") as rules_file:
                rules_json: json = json.load(rules_file)

        except Exception as e:
            print(e)

        if setting_mode == "default":
            self.__rules = copy.deepcopy(rules_json)
            self.__rule_items = list(self.__rules.keys())
        
        else:
            for rule_json_item in rules_json.keys():
                item_validation: bool = self.validation_rule_item(rule_json_item)
                if item_validation:
                    value_validation: bool = self.validation_rule_value(rule_json_item, rules_json.get(rule_json_item))
                
                else:
                    break
                
                if value_validation:
                    self.__rules[rule_json_item] = rules_json.get(rule_json_item)

                else:
                    break

    def validation_rule_item(self, rule: str) -> bool:
        if self.__debug:
            print("validation_rule_item")
        
        validation = False
        for rule_item in self.__rule_items:
            if rule_item == rule:
                validation = True

        if not validation:
            print(f"Validation Err {rule}: This rule is invalid")
        
        return validation

    def validation_rule_value(self, item:str, value: any) -> bool:
        if self.__debug:
            print("validation_rule_value")
        
        return True

    def get_rule_value(self, rule: str) -> any:
        if self.__debug:
            print("get_rule_value")

        validation:bool = self.validation_rule_item(rule)
        if validation:
            return self.__rules.get(rule)


    def __init__(self, rule_file_path:str=None, debug:bool=__debug):
        if debug:
            self.__debug = debug
            print("SettingRules.__init__")
        
        self.setting_rules()

        if rule_file_path:
            self.setting_rules(rule_file_path)