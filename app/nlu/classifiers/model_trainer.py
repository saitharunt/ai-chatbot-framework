import os
import logging
from app import configuration as config
import fasttext

logger = logging.getLogger(__name__)

pwd = os.path.dirname(os.path.abspath(os.path.join(__file__, '..', '..')))

logger = logging.getLogger(__name__)
cancel_class_keywords = config.cancel_class_keywords
return_class_keywords = config.return_class_keywords
confirmation_class_keywords = config.confirmation_class_keywords

class Classifier:
    def __init__(self):
        self.training_data = pwd + "/" + config.training_data
        self.model_path = pwd + "/" + config.model_path

    def train(self):
        try:
            self._model = fasttext.supervised(self.training_data, self.model_path, bucket=2000000, word_ngrams=2)
        except Exception as e:
            logger.error("Error while training classifier %s" % str(e))

    def predict(self, query):
        category = "error"
        if self._model:
            try:
                query = query.strip().lower()
                class_probabilites = dict(self._model.predict_proba([query], 5)[0])
                categories = self._model.predict([query], 5)[0]
                logger.info(class_probabilites)
                detected_cancel_keyword = False
                detected_return_keyword = False
                detect_confirm_keyword = False
                for token in query.split():
                    if token in cancel_class_keywords:
                        detected_cancel_keyword = True
                    elif token in return_class_keywords:
                        detected_return_keyword = True
                    elif token in confirmation_class_keywords:
                        detect_confirm_keyword = True
                if detect_confirm_keyword:
                    return ("order_confirmation", 1)

                else:
                    categories.remove("order_confirmation")

                if detected_cancel_keyword and detected_return_keyword:
                    return ("order_return_cancel", 1)

                else:
                    categories.remove("order_return_cancel")

                if detected_cancel_keyword:
                    return ("order_cancel", 1)

                else:
                    categories.remove("order_cancel")

                if detected_return_keyword:
                    return ("order_return", 1)

                else:
                    categories.remove("order_return")

                return (categories[0], class_probabilites[categories[0]])

            except Exception as e:
                logger.error("Error while predicting category %s" % str(e))
        return category

    def process(self, query):
        intent_id,confidence = self.predict(query)
        intent = {"intent": intent_id,
                  "confidence": confidence}
        intent_ranking = [{"intent": intent_id,
                           "confidence": confidence}]
        return intent, intent_ranking
