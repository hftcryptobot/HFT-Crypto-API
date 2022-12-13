from pydantic import BaseModel
import pprint


class ValidateBaseModel(BaseModel, validate_assignment=True):
    """
    This model simply sets up BaseModel with the validate_assignment flag to True
    """

    def __repr__(self):
        return pprint.pformat(self.dict(), indent=4)