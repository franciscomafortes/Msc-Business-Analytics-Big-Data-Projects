from optparse import OptionParser
import traceback

from error import OptionParserError
from settings import USAGE, default_source, default_option, default_destination
from settings import default_period, default_interval


class OptParser:
    @classmethod
    def parseopts(self):
        try:
            parser = OptionParser(usage = USAGE)

            parser.add_option("-s", "--source", action = "store",
                                            type = "string",
                                            help = "Choose stocks or twitter",
                                            dest = "source",
                                            default = default_source
                             )
            parser.add_option("-o", "--option", action = "store",
                                                  type = "string",
                                                  help = "Tickers to get data for stock or tweet to search for twitter",
                                                  dest = "option",
                                                  default = default_option
                             )
            parser.add_option("-p", "--period", action = "store",
                                                  type = "string",
                                                  help = "period for data to fetch",
                                                  dest = "period",
                                                  default = default_period
                             )
            parser.add_option("-i", "--interval", action = "store",
                                                 type = "string",
                                                 help = "interval for data to fetch",
                                                 dest = "interval",
                                                 default = default_interval
                             )
            parser.add_option("-d", "--destination", action = "store",
                                                    type = "string",
                                                    help = "destination for data kafka or file or screen",
                                                    dest = "destination",
                                                    default = default_destination
                             )
            parser.add_option("-D", "--counsumer_destination", action = "store",
                                                    type = "string",
                                                    help = "counsumer_destination for data influx or file or screen",
                                                    dest = "counsumer_destination",
                                                    default = "influx"
                             )
            parser.add_option("-t", "--topic", action = "store",
                                                    type = "string",
                                                    help = "kafka topic",
                                                    dest = "topic",
                             )
            parser.add_option("-r", "--realtime", action = "store",
                                                    type = "string",
                                                    help = "realtime data",
                                                    dest = "realtime",
                                                    default = False
                             )
            try:
                (options, args) = parser.parse_args()
            except:
                raise OptionParserError

            kwargs = {
                "source": options.source,
                "option": options.option,
                "period": options.period,
                "interval": options.interval,
                "destination": options.destination,
                "counsumer_destination": options.counsumer_destination,
                "topic": options.topic,
                "realtime": options.realtime
            }
            return kwargs
            raise OptionParserError
        except OptionParserError:
            raise OptionParserError('Type -h for help \n\t %s' % USAGE)
        except:
            raise OptionParserError(traceback.format_exc())