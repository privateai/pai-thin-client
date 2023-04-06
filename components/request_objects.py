import inspect
from typing import Dict, List


class BaseRequestObject:

    def to_dict(self):
        dict_obj = dict()
        for key, value in self.__dict__.items():
            if inspect.isclass(type(value)) and issubclass(type(value), BaseRequestObject):
                dict_obj[key[1:]] = value.to_dict()
            elif not key.startswith('__') and not callable(key):
                dict_obj[key[1:]] = value
        return dict_obj

    @classmethod
    def _fromdict(cls,
                 values: dict):
        return cls(**values)

class FilterSelector(BaseRequestObject):

    def __init__(self,):
        pass

class EntityTypeSelector(BaseRequestObject):

    def __init__(self,
                 ):
        pass

class EntityDetection(BaseRequestObject):
    default_accuracy = "high"
    default_return_entity = True
    valid_accuracies = ["standard", "standard_high", "standard_high_multilinguals", "high", "high_multilingual"]

    def __init__(self,
                 accuracy: str = default_accuracy,
                 entity_types: List[EntityTypeSelector] = [],
                 filter: List[FilterSelector] = [],
                 return_entity: bool = default_return_entity
    ):
        if self._accuracy_validator(accuracy):
            self._accuracy = accuracy,
        if self._entity_types_validator(entity_types):
            self.entity_types = entity_types
        if self._filter_validator(filter):
            self.filter = filter
        if self._return_entity_validator(return_entity):
            self._return_entity = return_entity

    @property
    def accuracy(self):
        return self._accuracy
    
    @property
    def return_entity(self):
        return self._return_entity
    
    @accuracy.setter
    def accuracy(self, var):
        if self._accuracy_validator(var):
            self._accuracy = var
    
    @return_entity.setter
    def return_entity(self, var):
        if self._return_entity_validator(var):
            self._return_entity = var

    def _accuracy_validator(self, var):
        if var not in self.valid_accuracies:
            raise ValueError(f"{var} is not valid. EntityDetection.accuracy can only be one of the following values: {self.valid_accuracies}")
        return True
    
    def _entity_types_validator(self, var):
        if type(var) is not list:
            raise ValueError(f"{var} is not valid. EntityDetection.entity_types can only be a list")
        elif var and not all(isinstance(x, EntityTypeSelector) for x in var):
            raise ValueError(f"EntityDetection.entity_types can only contain EntityTypeSelector objects")
        return True

    def _filter_validator(self, var):
        if type(var) is not list:
            raise ValueError(f"{var} is not valid. EntityDetection.filter can only be a list")
        elif var and not all(isinstance(x, FilterSelector) for x in var):
            raise ValueError(f"EntityDetection.filter can only contain FilterSelector objects")
        return True

    def _return_entity_validator(self, var):
        if type(var) is not bool:
            raise ValueError(f"{var} is not valid. EntityDetection.return_entity can only be True or False")
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("EntityDetection can only accept the values 'accuracy', 'entity_types', 'filter' and 'return_entity'")

class ProcessText(BaseRequestObject):
    default_type = "MARKER"
    default_pattern = "[UNIQUE_NUMBERED_ENTITY_TYPE]"
    valid_types = ["MARKER", "MASK", "SYNTHETIC"]
    valid_patterns = ["BEST_ENTITY_TYPE", "ALL_ENTITY_TYPES", "UNIQUE_NUMBERED_ENTITY_TYPE"]
    
    def __init__(self,
                 type: str = default_type,
                 pattern: str = default_pattern             
    ):
        if self._type_validator(type):
            self._type = type
        if self._pattern_validator(pattern):
            self._pattern = pattern
    @property
    def type(self):
        return self._type
    
    @property
    def pattern(self):
        return self._pattern
    
    @type.setter
    def type(self, var):
        if self._type_validator(var):
            self._type = var
    
    @pattern.setter
    def pattern(self, var):
        if self._pattern_validator(var):
            self._pattern = var

    def _type_validator(self, var):

        if var not in self.valid_types:
            raise ValueError(f"{var} is not valid. ProcessText.type can only be one of the following values: {self.valid_types}")
        return True

    def _pattern_validator(self, var):
        if var not in self.valid_patterns and var[1:-1] not in self.valid_patterns:
            raise ValueError(f"{var} is not valid. ProcessText.pattern can only be one of the following values: {self.valid_patterns}")
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("ProcessText can only accept the values 'type' and 'pattern'")

class ProcessTextRequest(BaseRequestObject):

    def __init__(self, 
                 text: List[str], 
                 link_batch: bool = None,
                 entity_detection: EntityDetection = None,
                 process_text: ProcessText = ProcessText()
    ):
        self._text = text
        self._link_batch = link_batch
        self._entity_detection = entity_detection
        self._process_text = process_text

    # @property
    # def text(self):
    #     return self._text
    
    # @property
    # def link_batch(self):
    #     return self._link_batch
    
    # @property
    # def entity_detection(self):
    #     return self._entity_detection
    
    # @property
    # def process_text(self):
    #     return self._process_text
    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "entity_detection":
                    initializer_dict[key] = EntityDetection.fromdict(value)
                elif key == "process_text":
                    initializer_dict[key] = ProcessText.fromdict(value)
                else:
                    initializer_dict[key] = value
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("ProcessTextRequest can only accept the values 'text', 'link_batch', 'entity_detection' and 'process_text'")
    



