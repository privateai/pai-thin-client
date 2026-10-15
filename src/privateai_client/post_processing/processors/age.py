class AgeEntityBucketProcessor:
    """
    Bin age entities found by the DEID container into consistently sized buckets.
    """

    def __init__(self, bin_size: int):
        """
        Initialize the AgeEntityBucketProcessor.

         Args:
            bin_size: the size of each bin (measured in years) used to bucket ages. Buckets start at age zero and
                progress in multiple of the bin_size.
        """
        self.bin_size = bin_size

    def __call__(self, entity: dict) -> str:
        """
        Process individual age entities into buckets.

        Args:
            entity: an individual entity returned by the DEID container.

        Examples:
            >>> text = [A 32-year old wants to travel.]
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
            >>> entity_processors = {"AGE": AgeEntityBucketProcessor(bin_size=5)}
            >>> anon_text_blocks = deidentify_text(
                    text,
                    resp,
                    entity_processors=entity_processors,
                    default_processor=MarkerEntityProcessor()
                )
            >>> anon_text_blocks
                ["A [30-34]-year old wants to travel."]
        """
        formatted_age = entity["analysis_result"].get("formatted")
        if not formatted_age:
            return "[%-%]"

        start_age = (formatted_age // self.bin_size) * self.bin_size
        end_age = start_age + self.bin_size
        return f"[{start_age}-{end_age-1}]"
