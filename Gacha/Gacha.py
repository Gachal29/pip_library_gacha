import random
import csv, json
import SettingRules

class Generate:
    __debug: bool = False

    __contents: list[dict[str:any]] = None

    __thema: str = None
    __main_content_column: str = None
    __result_format: str = None
    __sequencing: bool = None
    __build_flag: bool = None
    __build_flag_rule: dict[str:bool] = None
    __build_flag_column: str = None
    __build_flag_value: str = None
    __content_num_manage: bool = None
    __content_num_manage_rule: dict[str:bool] = None
    __content_num_manage_column: str = None
    __content_num_manage_fluctuation: int = None

    def __init__(self, contents:any=None, rules:str=None, debug:bool=__debug):
        if debug:
            self.__debug = debug
            print("Generator.__init__")

        if not contents:
            return print("No gacha contents")

        __setting_rules: SettingRules = SettingRules.SettingRules(rules, self.__debug)

        # rules
        self.__thema = __setting_rules.get_rule_value("thema")
        self.__main_content_column = __setting_rules.get_rule_value("main_content_column")
        self.__result_format = __setting_rules.get_rule_value("result_format")
        self.__sequencing = __setting_rules.get_rule_value("sequencing")
        self.__build_flag = __setting_rules.get_rule_value("build_flag")
        if self.__build_flag:
            self.__build_flag_rule = __setting_rules.get_rule_value("build_flag_rule")
            self.__build_flag_column = __setting_rules.get_rule_value("build_flag_column")
            self.__build_flag_value = __setting_rules.get_rule_value("build_flag_value")
    
        self.__content_num_manage = __setting_rules.get_rule_value("content_num_manage")
        if self.__content_num_manage:
            self.__content_num_manage_rule = __setting_rules.get_rule_value("content_num_manage_rule")
            self.__content_num_manage_column = __setting_rules.get_rule_value("content_num_manage_column")
            self.__content_num_manage_fluctuation = __setting_rules.get_rule_value("content_num_manage_fluctuation")

        if type(contents) is str:
            if contents.endswith(".csv"):
                contents = self.csv2contents(contents)

            elif contents.endswith(".json"):
                contents = self.json2contents(contents)

        if type(contents) is list:
            contents_validation: bool = self.validation_contents(contents)
            if contents_validation:
                self.__contents = contents

    def gachal(self) -> any:
        if self.__debug:
            print("gachal")

        if not self.__contents:
            return print("Err: No gacha contents")

        fact_contents: list[dict[str:any]] = []
        if self.__build_flag:
            for content in self.__contents:
                if not content[self.__build_flag_column] == self.__build_flag_value:
                    fact_contents.append(content)

        else:
            fact_contents = self.__contents

        if not fact_contents:
            return print("There is no gacha content to be discharged")

        if self.__sequencing:
            result = random.sample(fact_contents, len(fact_contents))

        else:
            result = random.choice(fact_contents)  

        if not self.__sequencing:
            result_index: int = self.__contents.index(result)
        
        if self.__content_num_manage:
            if self.__content_num_manage_rule["up"]:
                self.__contents[result_index][self.__content_num_manage_column] += self.__content_num_manage_fluctuation

            elif self.__content_num_manage_rule["down"]:
                self.__contents[result_index][self.__content_num_manage_column] -= self.__content_num_manage_fluctuation

        if self.__build_flag:
            if self.__build_flag_rule["appeared"]:
                self.__contents[result_index][self.__build_flag_column] = self.__build_flag_value

            elif self.__build_flag_rule["not_content_num"]:
                if self.__contents[result_index][self.__content_num_manage_column] == 0:
                    self.__contents[result_index][self.__build_flag_column] = self.__build_flag_value

        if self.__result_format == "main_only":
            return result[self.__main_content_column]
        
        return result

    def validation_contents(self, contents: list[dict[str:any]]) -> bool:
        if self.__debug:
            print("validation_contents")

        validation: bool = False
        if not type(contents) is list:
            print("Validation Err: Wrong contents format")
            return validation

        for content in contents:
            if not type(content) is dict:
                print("Validation Err: Wrong content format")
                break
            
            columns = content.keys()
            if not self.__main_content_column in columns:
                print("Validation Err: Missing main content column")
                break

            if self.__build_flag and not self.__build_flag_column in columns:
                print("Validation Err: Missing build flag column")
                break

            if self.__content_num_manage:
                if not self.__content_num_manage_column in columns:
                    print("Validation Err: Missing content num manage column")
                    break

                if not type(content[self.__content_num_manage_column]) is int:
                    content[self.__content_num_manage_column] = 0

            validation = True

        return validation

    def get_thema(self):
        return self.__thema

    def csv2contents(self, csv_path: str) -> list[dict[str:any]]:
        if self.__debug:
            print("csv2contents")

        contents: list[dict[str:any]] = []
        try:
            with open(csv_path, "r", encoding="utf-8-sig") as contents_file:
                csv_data: _csv.reader = csv.reader(contents_file)

                columns_data: bool = True
                for data in csv_data:
                    if columns_data:
                        columns: list[str] = data
                        columns_data = False
                        continue

                    content: dict[str:any] = {}
                    for i,column in enumerate(columns):
                        content[column] = data[i]
                    
                    contents.append(content)

        except Exception as e:
            print(e)

        return contents

    def json2contents(self, json_path: str) -> dict[str:any]:
        if self.__debug:
            print("json2contents")

        with open(json_path, "r", encoding="utf-8-sig") as json_file:
                contents: json = json.load(json_file)

        return contents

if __name__ == "__main__":
    gacha = Generate("./test_contents/test_contents.csv", "./test_contents/rules.json", True)
    print(gacha.gachal())
