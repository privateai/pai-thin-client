from dateutil.relativedelta import relativedelta


class DateShiftProcessor:
    """
    Scales dates by a defined offset.
    """

    def __init__(
        self,
        date_offset: relativedelta,
        operation: str = "add",
        date_format: str = "%Y-%m-%d",
    ):
        """
        Initialize the DateShiftProcessor.

        Args:
            date_offset: a date offset to apply to all dates.
            operation:denotes whether the offset is added/subtracted from the original date.
            date_format: a python date code used to format the outputted dates.
        """
        # validate operation values
        valid_operations = ["add", "subtract"]
        if operation in valid_operations:
            self._operation = operation
        else:
            raise ValueError(f"The operation {operation} does not exist")
        # initialize offset and date formats
        self._offset = date_offset
        self._date_format = date_format

    def __call__(self, entity: dict) -> str:
        """
        Process date entities by shifting them forward or backwards by a given factor

        Args:
            entity: an individual entity returned by the DEID container.

        Examples:
            >>> text = ["today is 1990-01-01."]
            >>> request = {
                "text": text,
                "entity_detection": {
                    "accuracy": "high",
                    "entity_types": [
                        {
                        "type": "ENABLE",
                        "value": ["AGE"]
                        }
                        ],
                    },
                }
            >>> text_request = AnalyzeTextRequest.from_dict(request)
            >>> # run analyze text
            >>> resp = client.analyze_text(text_request)
            >>> # run post-processing tasks
            >>> entity_processors = {"DATE": DateShiftProcessor(date_offset=relativedelta(months=3)}
            >>> anon_text_blocks = deidentify_text(
                    text,
                    resp,
                    entity_processors=entity_processors,
                    default_processor=MarkerEntityProcessor()
                )
            >>> anon_text_blocks
                ["today is 1990-04-01."]
        """
        pass


class DateBucketProcessor:
    """
    Bin date entities into defined buckets.
    """

    def __init__(self, date_bin: str, date_format: str = "%Y-%m-%d"):
        """
        Initialize the DateBucketProcessor.

        Args:
            date_bins: date compnents used to bin detected date entities. Acceptable values include "decade",
                "year", and "month".
            date_format: a python date code used to format the outputted dates.
        """
        # check for valid bin values
        valid_date_bins = ["decade", "year", "month"]
        if date_bin in valid_date_bins:
            self._date_bin = date_bin
        else:
            raise ValueError(f"date_bin value: {date_bin} is not a valid value")
        # initialize date formats
        self._date_format = date_format

    def __call__(self, entity: dict) -> str:
        """
        Process date entities by binning them into date buckets

        Args:
            entity: an individual entity returned by the DEID container.

        Examples:
            >>> text = ["today is 1990-01-01."]
            >>> request = {
                "text": text,
                "entity_detection": {
                    "accuracy": "high",
                    "entity_types": [
                        {
                        "type": "ENABLE",
                        "value": ["AGE"]
                        }
                        ],
                    },
                }
            >>> text_request = AnalyzeTextRequest.from_dict(request)
            >>> # run analyze text
            >>> resp = client.analyze_text(text_request)
            >>> # run post-processing tasks
            >>> entity_processors = {"DATE": DateBucketProcessor(date_bin="year")}
            >>> anon_text_blocks = deidentify_text(
                    text,
                    resp,
                    entity_processors=entity_processors,
                    default_processor=MarkerEntityProcessor()
                )
            >>> anon_text_blocks
                ["today is between 1990-01-01 and 1990-12-31."]
        """
        pass
