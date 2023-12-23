import datetime
import time

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import yfinance as yf
import matplotlib.pyplot as plt
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np


def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        return stock_data['Close']
    except Exception as e:
        print(e)
        return e, None


def get_stock_info(symbol):
    try:
        stock_info = yf.Ticker(symbol)
        return stock_info
    except Exception as e:
        print(e)
        return e


def get_req_data_keys():
    r_keys = ['sector', 'fullTimeEmployees', 'auditRisk', 'boardRisk', 'compensationRisk',
              'shareHolderRightsRisk', 'overallRisk', 'priceHint', 'previousClose', 'open',
              'dayLow',
              'dayHigh', 'regularMarketPreviousClose', 'regularMarketOpen', 'regularMarketDayLow',
              'regularMarketDayHigh', 'dividendRate', 'dividendYield', 'exDividendDate',
              'payoutRatio',
              'fiveYearAvgDividendYield', 'beta', 'trailingPE', 'forwardPE', 'volume',
              'regularMarketVolume', 'averageVolume', 'averageVolume10days',
              'averageDailyVolume10Day',
              'marketCap', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'priceToSalesTrailing12Months',
              'fiftyDayAverage', 'twoHundredDayAverage', 'trailingAnnualDividendRate',
              'trailingAnnualDividendYield', 'currency', 'enterpriseValue', 'profitMargins',
              'floatShares', 'sharesOutstanding', 'heldPercentInsiders', 'heldPercentInstitutions',
              'impliedSharesOutstanding', 'bookValue', 'priceToBook', 'earningsQuarterlyGrowth',
              'netIncomeToCommon', 'trailingEps', 'forwardEps', 'lastSplitFactor', 'lastSplitDate',
              'enterpriseToRevenue', 'enterpriseToEbitda', '52WeekChange', 'SandP52WeekChange',
              'lastDividendValue', 'longName', 'firstTradeDateEpochUtc', 'gmtOffSetMilliseconds',
              'targetHighPrice', 'targetLowPrice', 'targetMeanPrice',
              'targetMedianPrice', 'recommendationMean', 'recommendationKey',
              'numberOfAnalystOpinions',
              'totalCash', 'totalCashPerShare', 'ebitda', 'totalDebt', 'quickRatio', 'currentRatio',
              'totalRevenue', 'debtToEquity', 'revenuePerShare', 'returnOnAssets', 'returnOnEquity',
              'grossProfits', 'earningsGrowth', 'revenueGrowth', 'grossMargins', 'ebitdaMargins',
              'operatingMargins']
    return r_keys


def get_all_stocks():
    stock_list = ["RELIANCE.NS", "RELIANCE.BO", "TCS.BO", "TCS.NS", "HDFCBANK.BO", "HDFCBANK.NS",
                  "ICICIBANK.BO", "ICICIBANK.NS", "HINDUNILVR.NS", "HINDUNILVR.BO", "INFY.NS", "INFY.BO",
                  "BHARTIARTL.NS", "BHARTIARTL.BO", "ITC.BO", "ITC.NS", "SBIN.BO", "SBIN.NS", "BAJFINANCE.NS",
                  "BAJFINANCE.BO", "LT.NS", "LT.BO", "LICI.NS", "LICI.BO", "HCLTECH.NS", "HCLTECH.BO",
                  "KOTAKBANK.BO", "KOTAKBANK.NS", "AXISBANK.NS", "AXISBANK.BO", "MARUTI.NS", "MARUTI.BO",
                  "TITAN.NS", "TITAN.BO", "ASIANPAINT.NS", "ASIANPAINT.BO", "SUNPHARMA.BO", "SUNPHARMA.NS",
                  "ADANIENT.NS", "ADANIENT.BO", "BAJAJFINSV.NS", "BAJAJFINSV.BO", "NTPC.BO", "NTPC.NS",
                  "ULTRACEMCO.BO", "ULTRACEMCO.NS", "DMART.NS", "DMART.BO", "TATAMOTORS.NS", "TATAMOTORS.BO",
                  "TATAMTRDVR.NS", "TATAMTRDVR.BO", "ONGC.BO", "ONGC.NS", "NESTLEIND.BO", "NESTLEIND.NS",
                  "COALINDIA.BO", "COALINDIA.NS", "WIPRO.NS", "WIPRO.BO", "M&M.BO", "M&M.NS", "JSWSTEEL.BO",
                  "JSWSTEEL.NS", "POWERGRID.NS", "POWERGRID.BO", "ADANIPORTS.NS", "ADANIPORTS.BO", "BAJAJ",
                  "BAJAJ", "ADANIPOWER.NS", "ADANIPOWER.BO", "LTIM.NS", "LTIM.BO", "HAL.NS", "HAL.BO",
                  "ADANIGREEN.NS", "ADANIGREEN.BO", "TATASTEEL.BO", "TATASTEEL.NS", "IOC.BO", "IOC.NS",
                  "DLF.NS", "DLF.BO", "HDFCLIFE.NS", "HDFCLIFE.BO", "JIOFIN.NS", "JIOFIN.BO", "SBILIFE.BO",
                  "SBILIFE.NS", "VBL.BO", "VBL.NS", "SIEMENS.BO", "SIEMENS.NS", "GRASIM.BO", "GRASIM.NS",
                  "PIDILITIND.BO", "PIDILITIND.NS", "HINDZINC.BO", "HINDZINC.NS", "PFC.NS", "PFC.BO",
                  "BRITANNIA.NS", "BRITANNIA.BO", "TECHM.NS", "TECHM.BO", "INDUSINDBK.BO", "INDUSINDBK.NS",
                  "HINDALCO.BO", "HINDALCO.NS", "BEL.BO", "BEL.NS", "EICHERMOT.BO", "EICHERMOT.NS", "INDIGO.BO",
                  "INDIGO.NS", "GODREJCP.NS", "GODREJCP.BO", "BANKBARODA.BO", "BANKBARODA.NS", "DIVISLAB.NS",
                  "DIVISLAB.BO", "TRENT.NS", "TRENT.BO", "ZOMATO.NS", "ZOMATO.BO", "IRFC.NS", "IRFC.BO",
                  "RECLTD.NS", "RECLTD.BO", "SHREECEM.NS", "SHREECEM.BO", "CIPLA.NS", "CIPLA.BO", "DABUR.NS",
                  "DABUR.BO", "DRREDDY.NS", "DRREDDY.BO", "ADANIENSOL.BO", "ADANIENSOL.NS", "CHOLAFIN.BO",
                  "CHOLAFIN.NS", "BPCL.NS", "BPCL.BO", "ABB.NS", "ABB.BO", "TVSMOTOR.NS", "TVSMOTOR.BO",
                  "GAIL.BO", "GAIL.NS", "VEDL.NS", "VEDL.BO", "PNB.NS", "PNB.BO", "LODHA.NS", "LODHA.BO",
                  "TATAPOWER.NS", "TATAPOWER.BO", "AMBUJACEM.BO", "AMBUJACEM.NS", "TATACONSUM.BO",
                  "TATACONSUM.NS", "HAVELLS.NS", "HAVELLS.BO", "BAJAJHLDNG.BO", "BAJAJHLDNG.NS", "UNIONBANK.BO",
                  "UNIONBANK.NS", "ICICIPRULI.NS", "ICICIPRULI.BO", "APOLLOHOSP.NS", "APOLLOHOSP.BO",
                  "POLYCAB.NS", "POLYCAB.BO", "ATGL.NS", "ATGL.BO", "MANKIND.NS", "MANKIND.BO", "MCDOWELL",
                  "SHRIRAMFIN.BO", "SHRIRAMFIN.NS", "HEROMOTOCO.NS", "HEROMOTOCO.BO", "IOB.NS", "IOB.BO",
                  "CANBK.NS", "CANBK.BO", "TORNTPHARM.BO", "TORNTPHARM.NS", "ICICIGI.NS", "ICICIGI.BO",
                  "SRF.NS", "SRF.BO", "JINDALSTEL.NS", "JINDALSTEL.BO", "SBICARD.NS", "SBICARD.BO",
                  "JSWENERGY.BO", "JSWENERGY.NS", "CGPOWER.NS"]
    stock_list = ["AAVAS.NS", "AFFLE.NS", "AMBUJACEM.NS", "BANKBARODA.NS", "BANKINDIA.NS",
                  "BANSWRAS.NS", "BEL.NS", "BORORENEW.NS", "BCG.NS", "CDSL.NS", "CAMS.NS",
                  "CARERATING.NS", "CESC.NS", "DLINKINDIA.NS", "DATAMATICS.NS", "DCW.NS", "DEEPAKFERT.NS",
                  "DEEPAKNTR.NS", "DELTACORP.NS", "DBOL.NS", "DHAMPURSUG.NS", "DHANUKA.NS", "DVL.NS", "DIXON.NS",
                  "FINOLEXIND.NS", "GNFC.NS", "GSFC.NS", "GEOJITFSL.NS", "GLAND.NS", "GNA.NS",
                  "GPIL.NS", "GREENPLY.NS", "GUJGASLTD.NS", "HAPPSTMNDS.NS", "HAVELLS.NS", "HEG.NS", "HERANBA.NS",
                  "INFIBEAM.NS", "INFOBEAN.NS", "INFY.NS", "IOLCP.NS", "JKLAKSHMI.NS", "JKPAPER.NS", "JKTYRE.NS",
                  "JUBLFOOD.NS", "KANCHI.BO", "KRBL.NS", "KRBL.NS", "LT.NS", "LIBERTSHOE.NS",
                  "MANALIPETC.NS", "MIDHANI.NS", "NATIONALUM.NS", "NMDC.NS", "NSLNISP.NS", "NRBBEARING.NS", "NTPC.NS",
                  "NURECA.NS", "ONGC.NS", "ONMOBILE.NS", "PARAS.NS", "PENIND.NS", "PTC.NS",
                  "RCF.NS", "RVNL.NS", "RAJESHEXPO.NS", "RALLIS.NS", "RECLTD.NS", "RELIANCE.NS", "RUPA.NS", "SAIL.NS",
                  "SANOFI.NS", "SIS.NS", "SNOWMAN.NS", "SONACOMS.NS", "SONATSOFTW.NS", "STERLINBIO.NS", "STOVEKRAFT.NS",
                  "TANLA.NS", "TATACHEM.NS", "TATAELXSI.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TCS.NS", "TEJASNET.NS",
                  "TV18BRDCST.NS", "UNIONBANK.NS", "UPL.NS", "VEDL.NS", "IDEA.NS"]
    full_stock_list = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "HINDUNILVR.NS", "INFY.NS", "HDFC.NS",
                       "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "BAJFINANCE.NS", "LICI.NS", "LT.NS",
                       "HCLTECH.NS", "ASIANPAINT.NS", "AXISBANK.NS", "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS",
                       "DMART.NS", "ULTRACEMCO.NS", "BAJAJFINSV.NS", "WIPRO.NS", "ADANIENT.NS", "ONGC.NS", "NTPC.NS",
                       "JSWSTEEL.NS", "POWERGRID.NS", "M&M.NS", "LTIM.NS", "TATAMOTORS.NS", "ADANIGREEN.NS",
                       "ADANIPORTS.NS", "COALINDIA.NS", "TATASTEEL.NS", "HINDZINC.NS", "PIDILITIND.NS", "SIEMENS.NS",
                       "ADANITRANS.NS", "SBILIFE.NS", "IOC.NS", "BAJAJ-AUTO.NS", "GRASIM.NS", "TECHM.NS", "HDFCLIFE.NS",
                       "BRITANNIA.NS", "VEDL.NS", "GODREJCP.NS", "DABUR.NS", "ATGL.NS", "SHREECEM.NS", "HAL.NS",
                       "HINDALCO.NS", "VBL.NS", "DLF.NS", "BANKBARODA.NS", "INDUSINDBK.NS", "EICHERMOT.NS",
                       "DRREDDY.NS", "DIVISLAB.NS", "BPCL.NS", "HAVELLS.NS", "ADANIPOWER.NS", "INDIGO.NS", "CIPLA.NS",
                       "AMBUJACEM.NS", "SRF.NS", "ABB.NS", "BEL.NS", "SBICARD.NS", "GAIL.NS", "BAJAJHLDNG.NS",
                       "TATACONSUM.NS", "ICICIPRULI.NS", "CHOLAFIN.NS", "MARICO.NS", "APOLLOHOSP.NS", "TATAPOWER.NS",
                       "BOSCHLTD.NS", "BERGEPAINT.NS", "JINDALSTEL.NS", "MCDOWELL-N.NS", "UPL.NS", "AWL.NS",
                       "ICICIGI.NS", "TORNTPHARM.NS", "CANBK.NS", "PNB.NS", "TVSMOTOR.NS", "ZYDUSLIFE.NS", "TIINDIA.NS",
                       "TRENT.NS", "IDBI.NS", "NAUKRI.NS", "SHRIRAMFIN.NS", "HEROMOTOCO.NS", "INDHOTEL.NS", "PIIND.NS",
                       "IRCTC.NS", "CGPOWER.NS", "UNIONBANK.NS", "MOTHERSON.NS", "CUMMINSIND.NS", "SCHAEFFLER.NS",
                       "LODHA.NS", "ZOMATO.NS", "PGHH.NS", "YESBANK.NS", "POLYCAB.NS", "MAXHEALTH.NS", "IOB.NS",
                       "PAGEIND.NS", "COLPAL.NS", "ASHOKLEY.NS", "ALKEM.NS", "NHPC.NS", "PAYTM.NS", "PFC.NS",
                       "JSWENERGY.NS", "MUTHOOTFIN.NS", "AUBANK.NS", "INDUSTOWER.NS", "BALKRISIND.NS", "UBL.NS",
                       "ABCAPITAL.NS", "TATAELXSI.NS", "DALBHARAT.NS", "HDFCAMC.NS", "INDIANB.NS", "ASTRAL.NS",
                       "BHARATFORG.NS", "LTTS.NS", "MRF.NS", "TATACOMM.NS", "NYKAA.NS", "CONCOR.NS", "PERSISTENT.NS",
                       "PATANJALI.NS", "IRFC.NS", "LINDEINDIA.NS", "IDFCFIRSTB.NS", "PETRONET.NS", "SOLARINDS.NS",
                       "SAIL.NS", "MPHASIS.NS", "HINDPETRO.NS", "APLAPOLLO.NS", "FLUOROCHEM.NS", "NMDC.NS", "HONAUT.NS",
                       "SUPREMEIND.NS", "GUJGASLTD.NS", "BANDHANBNK.NS", "ACC.NS", "OBEROIRLTY.NS", "BANKINDIA.NS",
                       "RECLTD.NS", "AUROPHARMA.NS", "STARHEALTH.NS", "IGL.NS", "LUPIN.NS", "UCOBANK.NS", "JUBLFOOD.NS",
                       "POLICYBZR.NS", "GODREJPROP.NS", "M&MFIN.NS", "IDEA.NS", "OFSS.NS", "FEDERALBNK.NS",
                       "MANYAVAR.NS", "UNOMINDA.NS", "AIAENG.NS", "THERMAX.NS", "OIL.NS", "VOLTAS.NS", "3MINDIA.NS",
                       "COROMANDEL.NS", "SUNDARMFIN.NS", "KPITTECH.NS", "DEEPAKNTR.NS", "ESCORTS.NS", "BIOCON.NS",
                       "TATACHEM.NS", "TORNTPOWER.NS", "GMRINFRA.NS", "BHEL.NS", "SONACOMS.NS", "DELHIVERY.NS",
                       "SYNGENE.NS", "CRISIL.NS", "GICRE.NS", "COFORGE.NS", "PHOENIXLTD.NS", "JKCEMENT.NS",
                       "POONAWALLA.NS", "GLAXO.NS", "MFSL.NS", "METROBRAND.NS", "MSUMI.NS", "SUMICHEM.NS", "RELAXO.NS",
                       "NAVINFLUOR.NS", "SKFINDIA.NS", "CENTRALBK.NS", "GLAND.NS", "KANSAINER.NS", "GRINDWELL.NS",
                       "TIMKEN.NS", "IPCALAB.NS", "SUNDRMFAST.NS", "ATUL.NS", "ZEEL.NS", "L&TFH.NS", "ABFRL.NS",
                       "APOLLOTYRE.NS", "KPRMILL.NS", "ZFCVINDIA.NS", "FORTIS.NS", "AARTIIND.NS", "HATSUN.NS",
                       "CARBORUNIV.NS", "CROMPTON.NS", "VINATIORGA.NS", "IIFL.NS", "BATAINDIA.NS", "BDL.NS",
                       "LICHSGFIN.NS", "RAJESHEXPO.NS", "RAMCOCEM.NS", "ENDURANCE.NS", "DEVYANI.NS", "PSB.NS",
                       "DIXON.NS", "KAJARIACER.NS", "WHIRLPOOL.NS", "MAHABANK.NS", "SUNTV.NS", "PEL.NS", "PRESTIGE.NS",
                       "NIACL.NS", "RADICO.NS", "PFIZER.NS", "NH.NS", "EMAMILTD.NS", "LAURUSLABS.NS", "FIVESTAR.NS",
                       "AJANTPHARM.NS", "INDIAMART.NS", "360ONE.NS", "KEI.NS", "JBCHEPHARM.NS", "LALPATHLAB.NS",
                       "JSL.NS", "IRB.NS", "EXIDEIND.NS", "PVR.NS", "GSPL.NS", "BLUEDART.NS", "NATIONALUM.NS",
                       "RVNL.NS", "CREDITACC.NS", "TRIDENT.NS", "POWERINDIA.NS", "MEDANTA.NS", "GILLETTE.NS",
                       "RATNAMANI.NS", "ELGIEQUIP.NS", "ISEC.NS", "CGCL.NS", "GODREJIND.NS", "CLEAN.NS", "MAZDOCK.NS",
                       "MAHINDCIE.NS", "AEGISCHEM.NS", "FACT.NS", "BLUESTARCO.NS", "SANOFI.NS", "FINEORG.NS",
                       "AFFLE.NS", "GLENMARK.NS", "NAM-INDIA.NS", "SJVN.NS", "REDINGTON.NS", "AAVAS.NS", "IDFC.NS",
                       "FINCABLES.NS", "NUVOCO.NS", "BAJAJELEC.NS", "APTUS.NS", "SUVENPHAR.NS", "ASTERDM.NS", "RHIM.NS",
                       "KEC.NS", "SONATSOFTW.NS", "AETHER.NS", "DCMSHRIRAM.NS", "IEX.NS", "HAPPSTMNDS.NS", "KIMS.NS",
                       "ALKYLAMINE.NS", "CYIENT.NS", "CHAMBLFERT.NS", "ASAHIINDIA.NS", "CASTROLIND.NS", "BRIGADE.NS",
                       "KALYANKJIL.NS", "TTML.NS", "VGUARD.NS", "NLCINDIA.NS", "LAXMIMACH.NS", "TRITURBINE.NS",
                       "FINPIPE.NS", "AKZOINDIA.NS", "MANAPPURAM.NS", "EIHOTEL.NS", "CENTURYPLY.NS", "NATCOPHARM.NS",
                       "KIOCL.NS", "CHOLAHLDNG.NS", "CAMPUS.NS", "CAMS.NS", "AMARAJABAT.NS", "ZYDUSWELL.NS", "BASF.NS",
                       "TEJASNET.NS", "APLLTD.NS", "MGL.NS", "GRINFRA.NS", "ANGELONE.NS", "SFL.NS", "TTKPRESTIG.NS",
                       "APARINDS.NS", "HINDCOPPER.NS", "CDSL.NS", "GODFRYPHLP.NS", "RENUKA.NS", "CUB.NS",
                       "JKLAKSHMI.NS", "ANURAS.NS", "MRPL.NS", "GESHIP.NS", "POLYMED.NS", "NSLNISP.NS", "BIKAJI.NS",
                       "MOTILALOFS.NS", "ABSLAMC.NS", "CESC.NS", "TATAINVEST.NS", "ALLCARGO.NS", "KALPATPOWR.NS",
                       "PNBHOUSING.NS", "HUDCO.NS", "ITI.NS", "ROUTE.NS", "RITES.NS", "VTL.NS", "RBLBANK.NS", "HFCL.NS",
                       "KARURVYSYA.NS", "CERA.NS", "EIDPARRY.NS", "INGERRAND.NS", "GALAXYSURF.NS", "PPLPHARMA.NS",
                       "UTIAMC.NS", "KRBL.NS", "RAYMOND.NS", "ASTRAZEN.NS", "VIPIND.NS", "ACI.NS", "BALRAMCHIN.NS",
                       "SUZLON.NS", "GODREJAGRO.NS", "GNFC.NS", "ERIS.NS", "PGHL.NS", "MEDPLUS.NS", "SAPPHIRE.NS",
                       "DATAPATTNS.NS", "SUNCLAYLTD.NS", "JBMA.NS", "EASEMYTRIP.NS", "CCL.NS", "EQUITASBNK.NS",
                       "CHALET.NS", "RAINBOW.NS", "PNCINFRA.NS", "FSL.NS", "KSB.NS", "BSOFT.NS", "KNRCON.NS",
                       "SHOPERSTOP.NS", "SYMPHONY.NS", "CENTURYTEX.NS", "CANFINHOME.NS", "GRANULES.NS", "TANLA.NS",
                       "JYOTHYLAB.NS", "SPLPETRO.NS", "DEEPAKFERT.NS", "CRAFTSMAN.NS", "BIRLACORPN.NS", "BLS.NS",
                       "SHYAMMETL.NS", "NCC.NS", "GMMPFAUDLR.NS", "LATENTVIEW.NS", "USHAMART.NS", "HOMEFIRST.NS",
                       "JKPAPER.NS", "TMB.NS", "JINDWORLD.NS", "METROPOLIS.NS", "SAREGAMA.NS", "NBCC.NS", "ECLERX.NS",
                       "BALAMINES.NS", "WELSPUNIND.NS", "PRAJIND.NS", "COCHINSHIP.NS", "ZENSARTECH.NS", "AMBER.NS",
                       "LEMONTREE.NS", "PRINCEPIPE.NS", "TRIVENI.NS", "GARFIBRES.NS", "LXCHEM.NS", "STLTECH.NS",
                       "CEATLTD.NS", "BSE.NS", "SPARC.NS", "ALOKINDS.NS", "ORIENTELEC.NS", "INDIACEM.NS",
                       "JUBLINGREA.NS", "KIRLOSENG.NS", "TCIEXP.NS", "JMFINANCIL.NS", "NETWORK18.NS", "BBTC.NS",
                       "SWANENERGY.NS", "GPPL.NS", "KAYNES.NS", "VRLLOG.NS", "INTELLECT.NS", "SWSOLAR.NS",
                       "CHEMPLASTS.NS", "QUESS.NS", "ROLEXRINGS.NS", "MAHLIFE.NS", "ESABINDIA.NS", "MHRIL.NS",
                       "GOCOLORS.NS", "HGS.NS", "BORORENEW.NS", "GAEL.NS", "MAPMYINDIA.NS", "PRSMJOHNSN.NS",
                       "RUSTOMJEE.NS", "IRCON.NS", "RCF.NS", "WELCORP.NS", "BEML.NS", "GRSE.NS", "EPL.NS",
                       "MINDACORP.NS", "GRAPHITE.NS", "HGINFRA.NS", "OLECTRA.NS", "RELINFRA.NS", "JUSTDIAL.NS",
                       "RAIN.NS", "IONEXCHANG.NS", "EDELWEISS.NS", "UJJIVANSFB.NS", "TV18BRDCST.NS", "GPIL.NS",
                       "MTARTECH.NS", "TCI.NS", "RTNINDIA.NS", "VSTIND.NS", "SAFARI.NS", "ACE.NS", "MAHSCOOTER.NS",
                       "DELTACORP.NS", "GLS.NS", "GHCL.NS", "INDIGOPNTS.NS", "MAHSEAMLES.NS", "SUPRAJIT.NS",
                       "KFINTECH.NS", "GSFC.NS", "J&KBANK.NS", "RELIGARE.NS", "MASTEK.NS", "SIS.NS", "JINDALSAW.NS",
                       "TEGA.NS", "SYRMA.NS", "AVANTIFEED.NS", "STARCEMENT.NS", "IBULHSGFIN.NS", "RKFORGE.NS",
                       "CAPLIPOINT.NS", "VAIBHAVGBL.NS", "RBA.NS", "JUBLPHARMA.NS", "SHARDACROP.NS", "NIITLTD.NS",
                       "PCBL.NS", "MASFIN.NS", "SCI.NS", "PDSL.NS", "GUJALKALI.NS", "ELECON.NS", "CMSINFO.NS",
                       "VMART.NS", "ICRA.NS", "JSWHL.NS", "FDC.NS", "CSBBANK.NS", "KTKBANK.NS", "MMTC.NS",
                       "ENGINERSIN.NS", "SUNTECK.NS", "PRIVISCL.NS", "PARADEEP.NS", "SOBHA.NS", "FUSION.NS",
                       "GMDCLTD.NS", "VIJAYA.NS", "JAMNAAUTO.NS", "ANANTRAJ.NS", "SANSERA.NS", "MFL.NS", "AHLUCONT.NS",
                       "BSHSL.NS", "TATACOFFEE.NS", "TEAMLEASE.NS", "JKTYRE.NS", "VARROC.NS", "GREENLAM.NS",
                       "JPPOWER.NS", "INFIBEAM.NS", "SPANDANA.NS", "HSCL.NS", "BHARATRAS.NS", "RAJRATAN.NS",
                       "LAOPALA.NS", "SARDAEN.NS", "RALLIS.NS", "BOROLTD.NS", "RATEGAIN.NS", "SCHNEIDER.NS",
                       "RPOWER.NS", "ARVINDFASN.NS", "TATVA.NS", "POWERMECH.NS", "HCG.NS", "NESCO.NS", "HEIDELBERG.NS",
                       "TECHNOE.NS", "POLYPLEX.NS", "SURYAROSNI.NS", "AUTOAXLES.NS", "JWL.NS", "NFL.NS", "HEG.NS",
                       "RAJRILTD.NS", "CHENNPETRO.NS", "WSTCSTPAPR.NS", "LUXIND.NS", "HIKAL.NS", "MIDHANI.NS",
                       "HLEGLAS.NS", "SHAREINDIA.NS", "NOCIL.NS", "NAZARA.NS", "BANARISUG.NS", "ANANDRATHI.NS",
                       "PRUDENT.NS", "GRAVITA.NS", "GREENPANEL.NS", "VESUVIUS.NS", "DCBBANK.NS", "ROSSARI.NS",
                       "RESPONIND.NS", "TINPLATE.NS", "KIRLOSBROS.NS", "RAILTEL.NS", "AMIORG.NS", "ISGEC.NS",
                       "NEOGEN.NS", "MARKSANS.NS", "NAVA.NS", "NEWGEN.NS", "BECTORFOOD.NS", "TWL.NS", "AARTIDRUGS.NS",
                       "UJJIVAN.NS", "GATEWAY.NS", "SULA.NS", "DAAWAT.NS", "SOUTHBANK.NS", "GET&D.NS", "HARSHA.NS",
                       "PGEL.NS", "RSYSTEMS.NS", "INDOCO.NS", "MOLDTKPAC.NS", "IFBIND.NS", "SBCL.NS", "BCG.NS",
                       "GREAVESCOT.NS", "MOIL.NS", "TATASTLLP.NS", "TARSONS.NS", "SHANTIGEAR.NS", "CHOICEIN.NS",
                       "TIIL.NS", "DHANUKA.NS", "JCHAC.NS", "DODLA.NS", "DALMIASUG.NS", "VOLTAMP.NS", "ASTEC.NS",
                       "SUDARSCHEM.NS", "KSCL.NS", "SUNFLAG.NS", "IBREALEST.NS", "THOMASCOOK.NS", "HBLPOWER.NS",
                       "INOXWIND.NS", "NILKAMAL.NS", "ZENTEC.NS", "TCNSBRANDS.NS", "ADVENZYMES.NS", "STAR.NS", "FCL.NS",
                       "KKCL.NS", "HINDWAREAP.NS", "MAHLOG.NS", "EMIL.NS", "JTEKTINDIA.NS", "MANINFRA.NS", "ITDC.NS",
                       "APCOTEXIND.NS", "PRICOLLTD.NS", "PTC.NS", "AARTIPHARM.NS", "MBAPL.NS", "SAGCEM.NS",
                       "TDPOWERSYS.NS", "JAICORPLTD.NS", "DBL.NS", "BARBEQUE.NS", "UNIPARTS.NS", "UFLEX.NS",
                       "WONDERLA.NS", "PSPPROJECT.NS", "KIRLOSIND.NS", "IPL.NS", "DISHTV.NS", "TATAMETALI.NS",
                       "PAISALO.NS", "PFOCUS.NS", "HEMIPROP.NS", "LGBBROSLTD.NS", "MAITHANALL.NS", "SSWL.NS",
                       "NEULANDLAB.NS", "HATHWAY.NS", "THYROCARE.NS", "ORIENTCEM.NS", "DREAMFOLKS.NS", "ETHOSLTD.NS",
                       "GLOBUSSPR.NS", "GANESHHOUC.NS", "ARVIND.NS", "ICIL.NS", "SHRIPISTON.NS", "WOCKPHARMA.NS",
                       "DBREALTY.NS", "ISMTLTD.NS", "JINDALPOLY.NS", "WABAG.NS", "BAJAJCON.NS", "GENUSPOWER.NS",
                       "BUTTERFLY.NS", "NAVNETEDUL.NS", "GOKEX.NS", "APOLLOPIPE.NS", "LANDMARK.NS", "IFCI.NS",
                       "ATFL.NS", "EVEREADY.NS", "AGI.NS", "TI.NS", "ASHOKA.NS", "SOMANYCERA.NS", "HCC.NS",
                       "JISLJALEQS.NS", "VINDHYATEL.NS", "FIEMIND.NS", "TASTYBITE.NS", "JAYNECOIND.NS", "HONDAPOWER.NS",
                       "UNICHEMLAB.NS", "MUKANDLTD.NS", "CIGNITITEC.NS", "MMFL.NS", "VENKEYS.NS", "RAMKY.NS",
                       "DIVGIITTS.NS", "CAMLINFINE.NS", "SHILPAMED.NS", "GULFOILLUB.NS", "MOL.NS", "DOLLAR.NS",
                       "VSTTILLERS.NS", "SUBROS.NS", "DCAL.NS", "GABRIEL.NS", "MAXVIL.NS", "SIYSIL.NS", "TVSSRICHAK.NS",
                       "ASTRAMICRO.NS", "JKIL.NS", "JAGRAN.NS", "ELECTCAST.NS", "CARERATING.NS", "INDIAGLYCO.NS",
                       "BALMLAWRIE.NS", "KOLTEPATIL.NS", "IMAGICAA.NS", "WELENT.NS", "TIPSINDLTD.NS", "SWARAJENG.NS",
                       "MAYURUNIQ.NS", "GANECOS.NS", "PARAS.NS", "LUMAXTECH.NS", "ACCELYA.NS", "KESORAMIND.NS",
                       "CARTRADE.NS", "MPSLTD.NS", "SEQUENT.NS", "HIL.NS", "GUFICBIO.NS", "ITDCEM.NS", "PILANIINVS.NS",
                       "MSTCLTD.NS", "LSIL.NS", "PANAMAPET.NS", "OPTIEMUS.NS", "SIRCA.NS", "TIRUMALCHM.NS",
                       "DYNAMATECH.NS", "SUNDARMHLD.NS", "TIMETECHNO.NS", "DBCORP.NS", "ASHIANA.NS", "CONFIPET.NS",
                       "DIAMONDYD.NS", "NUCLEUS.NS", "GREENPLY.NS", "JPASSOCIAT.NS", "WENDT.NS", "FINOPB.NS",
                       "FMGOETZE.NS", "SANGHIIND.NS", "VAKRANGEE.NS", "GNA.NS", "AMRUTANJAN.NS", "EMUDHRA.NS",
                       "DATAMATICS.NS", "SHARDAMOTR.NS", "IOLCP.NS", "LUMAXIND.NS", "BAJAJHIND.NS", "STYLAMIND.NS",
                       "ANDHRAPAP.NS", "SOTL.NS", "ADFFOODS.NS", "VIDHIING.NS", "KABRAEXTRU.NS", "BEPL.NS", "RUPA.NS",
                       "NACLIND.NS", "VSSL.NS", "VISHNU.NS", "DWARKESH.NS", "DHANI.NS", "BANCOINDIA.NS", "KINGFA.NS",
                       "SUBEXLTD.NS", "HINDOILEXP.NS", "RTNPOWER.NS", "VADILALIND.NS", "BBOX.NS", "ORCHPHARMA.NS",
                       "PURVA.NS", "COSMOFIRST.NS", "IMFA.NS", "SUPRIYA.NS", "SAKSOFT.NS", "IIFLSEC.NS",
                       "SANGHVIMOV.NS", "GOKULAGRO.NS", "ALEMBICLTD.NS", "VENUSPIPES.NS", "SEAMECLTD.NS", "TNPL.NS",
                       "KPIGREEN.NS", "BFINVEST.NS", "SESHAPAPER.NS", "DHAMPURSUG.NS", "ANDHRSUGAR.NS", "KIRIINDUS.NS",
                       "TTKHLTCARE.NS", "CARYSIL.NS", "GOCLCORP.NS", "JSWISPL.NS", "STERTOOLS.NS", "SHALBY.NS",
                       "TIDEWATER.NS", "KRSNAA.NS", "KRISHANA.NS", "HUHTAMAKI.NS", "BBL.NS", "SEPC.NS", "ORISSAMINE.NS",
                       "FILATEX.NS", "THEJO.NS", "APTECHT.NS", "ORIENTHOT.NS", "DCXINDIA.NS", "FOSECOIND.NS",
                       "GOLDIAM.NS", "SHANKARA.NS", "INSECTICID.NS", "THANGAMAYL.NS", "SHK.NS", "TEXRAIL.NS",
                       "CANTABIL.NS", "GALLANTT.NS", "HERITGFOOD.NS", "KCP.NS", "MOREPENLAB.NS", "GATI.NS",
                       "RAMASTEEL.NS", "HESTERBIO.NS", "NRBBEARING.NS", "INDOSTAR.NS", "MONTECARLO.NS", "KSL.NS",
                       "KDDL.NS", "TCPLPACK.NS", "MARATHON.NS", "ARVSMART.NS", "DCW.NS", "DEN.NS", "STEELXIND.NS",
                       "EIHAHOTELS.NS", "IGPL.NS", "NITINSPIN.NS", "EXPLEOSOL.NS", "VERANDA.NS", "SALASAR.NS",
                       "STYRENIX.NS", "ADORWELD.NS", "BHAGCHEM.NS", "PCJEWELLER.NS", "GENESYS.NS", "STOVEKRAFT.NS",
                       "RANEHOLDIN.NS", "NDTV.NS", "XPROINDIA.NS", "MANORAMA.NS", "GRWRHITECH.NS", "HARIOMPIPE.NS",
                       "SANDHAR.NS", "AVTNPL.NS", "IWEL.NS", "SJS.NS", "EVERESTIND.NS", "FAIRCHEMOR.NS", "SASKEN.NS",
                       "OAL.NS", "NELCO.NS", "RIIL.NS", "SOLARA.NS", "TAJGVK.NS", "BOMDYEING.NS", "MANGCHEFER.NS",
                       "GOODLUCK.NS", "RPGLIFE.NS", "PATELENG.NS", "SPIC.NS", "INOXGREEN.NS", "GIPCL.NS",
                       "UNIVCABLES.NS", "NSIL.NS", "HMT.NS", "MATRIMONY.NS", "MTNL.NS", "SDBL.NS", "VALIANTORG.NS",
                       "ARMANFIN.NS", "REPCOHOME.NS", "HERANBA.NS", "BFUTILITIE.NS", "PRECWIRE.NS", "AXITA.NS",
                       "GRMOVER.NS", "GTPL.NS", "IGARASHI.NS", "INFOBEAN.NS", "ALICON.NS", "THEMISMED.NS", "TVTODAY.NS",
                       "WHEELS.NS", "RPSGVENT.NS", "RAMCOIND.NS", "SMLISUZU.NS", "AHL.NS", "UNIENTER.NS", "SATIN.NS",
                       "KUANTUM.NS", "GANESHBE.NS", "SUVEN.NS", "SATIA.NS", "GULPOLY.NS", "UGARSUGAR.NS",
                       "MANALIPETC.NS", "PIXTRANS.NS", "SHRIRAMPPS.NS", "RADIANTCMS.NS", "PNBGILTS.NS", "INDORAMA.NS",
                       "ASHAPURMIN.NS", "UGROCAP.NS", "AXISCADES.NS", "HITECH.NS", "PUNJABCHEM.NS", "SURYODAY.NS",
                       "EKC.NS", "JASH.NS", "DPSCLTD.NS", "TARC.NS", "BHARATWIRE.NS", "EXCELINDUS.NS", "SPECIALITY.NS",
                       "ANUP.NS", "SKIPPER.NS", "AJMERA.NS", "SHALPAINTS.NS", "GMBREW.NS", "SANGAMIND.NS",
                       "SHIVALIK.NS", "GMRP&UI.NS", "PENIND.NS", "GEOJITFSL.NS", "BCLIND.NS", "DBOL.NS", "SHAILY.NS",
                       "LIKHITHA.NS", "MADRASFERT.NS", "STEELCAS.NS", "MKPL.NS", "ROSSELLIND.NS", "KITEX.NS",
                       "PRAKASH.NS", "ARTEMISMED.NS", "RICOAUTO.NS", "OMAXE.NS", "CENTUM.NS", "ROTO.NS", "PRECAM.NS",
                       "BIGBLOC.NS", "SHREDIGCEM.NS", "CLSEL.NS", "GTLINFRA.NS", "PGIL.NS", "UTTAMSUGAR.NS",
                       "AVADHSUGAR.NS", "PITTIENG.NS", "5PAISA.NS", "NAHARSPING.NS", "SPCENET.NS", "SPORTKING.NS",
                       "DEEPINDS.NS", "PARAGMILK.NS", "AGARIND.NS", "CONTROLPR.NS", "BAJAJHCARE.NS", "KAMDHENU.NS",
                       "CHEMCON.NS", "GICHSGFIN.NS", "MEDICAMEQ.NS", "DLINKINDIA.NS", "ARIHANTSUP.NS", "VHL.NS",
                       "PFS.NS", "HEXATRADEX.NS", "RILINFRA.NS", "CAPACITE.NS", "SPAL.NS", "NCLIND.NS", "63MOONS.NS",
                       "NAVKARCORP.NS", "ORIENTPPR.NS", "DREDGECORP.NS", "AMBIKCO.NS", "CENTRUM.NS", "LINC.NS",
                       "RGL.NS", "SCHAND.NS", "NELCAST.NS", "FAZE3Q.NS", "KICL.NS", "DVL.NS", "JAGSNPHARM.NS",
                       "POKARNA.NS", "IFGLEXPOR.NS", "TRIL.NS", "CENTENKA.NS", "SMCGLOBAL.NS", "ROHLTD.NS",
                       "INDNIPPON.NS", "SHAKTIPUMP.NS", "NGLFINE.NS", "IMPAL.NS", "BLISSGVS.NS", "ALLSEC.NS",
                       "ORIENTBELL.NS", "MANGLMCEM.NS", "SANDESH.NS", "BODALCHEM.NS", "ESTER.NS", "ZOTA.NS", "RSWM.NS",
                       "INDRAMEDCO.NS", "QUICKHEAL.NS", "SRHHYPOLTD.NS", "AURIONPRO.NS", "GSLSU.NS", "SASTASUNDR.NS",
                       "MANAKSIA.NS", "AWHCL.NS", "BLKASHYAP.NS", "RAMRAT.NS", "JINDRILL.NS", "VIMTALABS.NS",
                       "CLOUD.NS", "DPABHUSHAN.NS", "MOLDTECH.NS", "ATULAUTO.NS", "KOKUYOCMLN.NS", "SIGACHI.NS",
                       "HIMATSEIDE.NS", "LINCOLN.NS", "GREENPOWER.NS", "EMAMIPAP.NS", "SATINDLTD.NS", "RAMCOSYS.NS",
                       "HPAL.NS", "OCCL.NS", "FOCUS.NS", "GEPIL.NS", "SUTLEJTEX.NS", "PANACEABIO.NS", "JAIBALAJI.NS",
                       "RML.NS", "JETAIRWAYS.NS", "TRACXN.NS", "KHAICHEM.NS", "TNPETRO.NS", "ONWARDTEC.NS",
                       "TFCILTD.NS", "ONMOBILE.NS", "INNOVANA.NS", "GANDHITUBE.NS", "TEXINFRA.NS", "MEDICO.NS",
                       "TVSELECT.NS", "HEUBACHIND.NS", "VINYLINDIA.NS", "PARACABLES.NS", "FOODSIN.NS", "HLVLTD.NS",
                       "COFFEEDAY.NS", "BETA.NS", "APEX.NS", "YUKEN.NS", "ELIN.NS", "MONARCH.NS", "DMCC.NS",
                       "CHEVIOT.NS", "XCHANGING.NS", "VISAKAIND.NS", "SUMMITSEC.NS", "SUKHJITS.NS", "INDIANHUME.NS",
                       "JUBLINDS.NS", "ASALCBR.NS", "DECCANCE.NS", "JAYBARMARU.NS", "COOLCAPS.NS", "APOLLO.NS",
                       "ELDEHSG.NS", "HERCULES.NS", "4THDIM.NS", "KRITI.NS", "AGSTRA.NS", "NAHARPOLY.NS", "MANINDS.NS",
                       "ENIL.NS", "SYNCOMF.NS", "KAMOPAINTS.NS", "NAGAFERT.NS", "SCPL.NS", "HPL.NS", "INDOAMIN.NS",
                       "DCMSRIND.NS", "MENONBE.NS", "VASCONEQ.NS", "VLSFINANCE.NS", "BALAXI.NS", "ZEEMEDIA.NS",
                       "CREATIVE.NS", "KRISHIVAL.NS", "SNOWMAN.NS", "KOPRAN.NS", "SHREYAS.NS", "REFEX.NS", "KSOLVES.NS",
                       "GFLLIMITED.NS", "SPECTRUM.NS", "RUSHIL.NS", "IRISDOREME.NS", "BINDALAGRO.NS", "SELMC.NS",
                       "BHAGERIA.NS", "ZUARI.NS", "TALBROAUTO.NS", "RUBYMILLS.NS", "OSWALSEEDS.NS", "DPWIRES.NS",
                       "SMSPHARMA.NS", "DHARMAJ.NS", "RBL.NS", "GOYALALUM.NS", "NRL.NS", "MIRZAINT.NS", "VIKASLIFE.NS",
                       "WINDLAS.NS", "HITECHGEAR.NS", "SHREEPUSHK.NS", "SPENCERS.NS", "KANORICHEM.NS", "JPOLYINVST.NS",
                       "ASAL.NS", "SILVERTUC.NS", "3IINFOLTD.NS", "MALLCOM.NS", "CREST.NS", "REPRO.NS", "MARINE.NS",
                       "KECL.NS", "DENORA.NS", "EXXARO.NS", "MAGADSUGAR.NS", "ASIANTILES.NS", "JAYAGROGN.NS",
                       "DIGISPICE.NS", "BBTCL.NS", "PREMEXPLN.NS", "SWELECTES.NS", "KELLTONTEC.NS", "MUTHOOTCAP.NS",
                       "APCL.NS", "ASIANENE.NS", "DONEAR.NS", "ADSL.NS", "BANSWRAS.NS", "NAHARCAP.NS", "ICEMAKE.NS",
                       "BAIDFIN.NS", "STCINDIA.NS", "TBZ.NS", "SALZERELEC.NS", "IFBAGRO.NS", "PTL.NS", "ARIHANTCAP.NS",
                       "CSLFINANCE.NS", "JSLL.NS", "UNIVPHOTO.NS", "HARDWYN.NS", "DSSL.NS", "REVATHI.NS",
                       "HCL-INSYS.NS", "PLASTIBLEN.NS", "UNIDT.NS", "CAREERP.NS", "ARROWGREEN.NS", "SREEL.NS", "SBC.NS",
                       "RADIOCITY.NS", "SERVOTECH.NS", "SAKAR.NS", "BALAJITELE.NS", "NXTDIGITAL.NS", "GOACARBON.NS",
                       "BIRLACABLE.NS", "RITCO.NS", "SELAN.NS", "ASCOM.NS", "OSIAHYPER.NS", "HINDCOMPOS.NS",
                       "DHANBANK.NS", "DYCL.NS", "DHUNINV.NS", "EIFFL.NS", "MUNJALAU.NS", "NAHARINDUS.NS",
                       "DELPHIFX.NS", "URJA.NS", "PRIMESECU.NS", "NECLIFE.NS", "NBIFIN.NS", "GRPLTD.NS", "MAWANASUG.NS",
                       "ZIMLAB.NS", "PDMJEPAPER.NS", "ONEPOINT.NS", "MAXIND.NS", "SHYAMCENT.NS", "VARDHACRLC.NS",
                       "RADHIKAJWE.NS", "NPST.NS", "THEINVEST.NS", "HTMEDIA.NS", "NRAIL.NS", "RCOM.NS", "DICIND.NS",
                       "OSWALAGRO.NS", "POCL.NS", "AARTISURF.NS", "SKMEGGPROD.NS", "SOLEX.NS", "DEEPENR.NS",
                       "FCSSOFT.NS", "MUNJALSHOW.NS", "KOTHARIPRO.NS", "PONNIERODE.NS", "CHEMBOND.NS", "USASEEDS.NS",
                       "KERNEX.NS", "RANASUG.NS", "CUPID.NS", "BGRENERGY.NS", "GENUSPAPER.NS", "GSS.NS", "PENINLAND.NS",
                       "JYOTISTRUC.NS", "ADVANIHOTR.NS", "KAYA.NS", "KOTHARIPET.NS", "LIBERTSHOE.NS", "KHADIM.NS",
                       "PPL.NS", "VIPCLOTHNG.NS", "NDRAUTO.NS", "PROZONINTU.NS", "INDOBORAX.NS", "CONSOFINVT.NS",
                       "INDSWFTLAB.NS", "ZUARIIND.NS", "GVKPIL.NS", "SBGLP.NS", "HIRECT.NS", "CHEMFAB.NS", "GLOBAL.NS",
                       "ANNAPURNA.NS", "INTLCONV.NS", "EMKAYTOOLS.NS", "ORBTEXP.NS", "SOUTHWEST.NS", "KAMATHOTEL.NS",
                       "RAJMET.NS", "RAMAPHO.NS", "OMINFRAL.NS", "HMVL.NS", "AYMSYNTEX.NS", "MSPL.NS", "WEALTH.NS",
                       "UNITECH.NS", "WEBELSOLAR.NS", "NURECA.NS", "LYKALABS.NS", "GKWLIMITED.NS", "MHLXMIRU.NS",
                       "AURUM.NS", "SKYGOLD.NS", "ALBERTDAVD.NS", "SHIVAUM.NS", "PAVNAIND.NS", "CINELINE.NS",
                       "KOTARISUG.NS", "SHEMAROO.NS", "SILINV.NS", "SKP.NS", "MMP.NS", "EQUIPPP.NS", "MANORG.NS",
                       "CYBERTECH.NS", "TRIGYN.NS", "SINTERCOM.NS", "JINDALPHOT.NS", "SARLAPOLY.NS", "RUCHIRA.NS",
                       "ESSENTIA.NS", "MACPOWER.NS", "AUTOIND.NS", "ORIENTABRA.NS", "APOLSINHOT.NS", "DYNPRO.NS",
                       "CLEDUCATE.NS", "PARSVNATH.NS", "GSCLCEMENT.NS", "MIRCELECTR.NS", "VISHWARAJ.NS",
                       "HINDMOTORS.NS", "NINSYS.NS", "NATHBIOGEN.NS", "KNAGRI.NS", "GEECEE.NS", "KCPSUGIND.NS",
                       "STEL.NS", "PODDARMENT.NS", "KOTYARK.NS", "HITECHCORP.NS", "EUROBOND.NS", "MICEL.NS",
                       "ORICONENT.NS", "20MICRONS.NS", "MWL.NS", "MINDTECK.NS", "BMETRICS.NS", "GOKUL.NS", "SECL.NS",
                       "DUGLOBAL.NS", "WEL.NS", "SUPERHOUSE.NS", "LOYALTEX.NS", "BPL.NS", "BIRLAMONEY.NS",
                       "GPTINFRA.NS", "E2E.NS", "SHIVAMAUTO.NS", "DCMNVL.NS", "MAZDA.NS", "MADHAVBAUG.NS",
                       "WINDMACHIN.NS", "BASML.NS", "WALCHANNAG.NS", "SEJALLTD.NS", "UCALFUEL.NS", "MAHEPC.NS",
                       "V2RETAIL.NS", "SAKUMA.NS", "VERTOZ.NS", "KMSUGAR.NS", "ASHIMASYN.NS", "UFO.NS", "VIKASECO.NS",
                       "SAKHTISUG.NS", "MAHESHWARI.NS", "MAANALU.NS", "HUBTOWN.NS", "REPL.NS", "QMSMEDI.NS",
                       "MANAKSTEEL.NS", "EMAMIREAL.NS", "GENCON.NS", "STARPAPER.NS", "GUJAPOLLO.NS", "JAYSREETEA.NS",
                       "NDL.NS", "BCONCEPTS.NS", "GIRRESORTS.NS", "SMLT.NS", "TPLPLASTEH.NS", "TEMBO.NS", "DANGEE.NS",
                       "NIPPOBATRY.NS", "ASIANHOTNR.NS", "BRNL.NS", "PPAP.NS", "PASUPTAC.NS", "FROG.NS", "ASAHISONG.NS",
                       "PRECOT.NS", "MEP.NS", "VENUSREM.NS", "KILITCH.NS", "BTML.NS", "MEGASTAR.NS", "DRCSYSTEMS.NS",
                       "ZODIACLOTH.NS", "HILTON.NS", "INDOTHAI.NS", "JITFINFRA.NS", "EROSMEDIA.NS", "DEVIT.NS",
                       "BIL.NS", "EIMCOELECO.NS", "ANMOL.NS", "COASTCORP.NS", "RAJTV.NS", "KORE.NS", "RELCAPITAL.NS",
                       "MGEL.NS", "FOCE.NS", "INDTERRAIN.NS", "TAKE.NS", "TOTAL.NS", "ACCURACY.NS", "AVG.NS",
                       "HARRMALAYA.NS", "SHREYANIND.NS", "LOKESHMACH.NS", "LGBFORGE.NS", "SYSTANGO.NS", "SIGMA.NS",
                       "MARALOVER.NS", "ABAN.NS", "BAFNAPH.NS", "BEDMUTHA.NS", "SIMPLEXINF.NS", "ARIES.NS", "DTIL.NS",
                       "KRITINUT.NS", "IVC.NS", "IITL.NS", "SWASTIK.NS", "AARON.NS", "VITAL.NS", "BEWLTD.NS",
                       "NILAINFRA.NS", "INDOTECH.NS", "PVP.NS", "AHLEAST.NS", "SAH.NS", "TIPSFILMS.NS", "PHANTOMFX.NS",
                       "DUCOL.NS", "KANPRPLA.NS", "VINNY.NS", "MCLEODRUSS.NS", "TRF.NS", "ALLETEC.NS", "MANOMAY.NS",
                       "INSPIRISYS.NS", "AIRAN.NS", "MODISONLTD.NS", "MURUDCERA.NS", "TIRUPATI.NS", "PAR.NS", "SGIL.NS",
                       "SPLIL.NS", "GEEKAYWIRE.NS", "PALREDTEC.NS", "ESSARSHPNG.NS", "SIL.NS", "PRITI.NS",
                       "AKSHARCHEM.NS", "RAMANEWS.NS", "RUCHINFRA.NS", "ALANKIT.NS", "MEGASOFT.NS", "IZMO.NS",
                       "GULFPETRO.NS", "TOUCHWOOD.NS", "SARVESHWAR.NS", "TARMAT.NS", "RPPL.NS", "IEL.NS",
                       "BHARATGEAR.NS", "GOLDTECH.NS", "MBLINFRA.NS", "PROPEQUITY.NS", "EMKAY.NS", "IL&FSENGG.NS",
                       "BSL.NS", "UNITEDPOLY.NS", "PASHUPATI.NS", "SHIVATEX.NS", "MANGALAM.NS", "KRISHNADEF.NS",
                       "PREMIERPOL.NS", "SMSLIFE.NS", "GOLDSTAR.NS", "BROOKS.NS", "VAISHALI.NS", "ALMONDZ.NS",
                       "3RDROCK.NS", "PRESSMN.NS", "AARVI.NS", "AKSHAR.NS", "LATTEYS.NS", "VISESHINFO.NS",
                       "BHAGYANGR.NS", "TTL.NS", "SADBHAV.NS", "COMPUSOFT.NS", "KAKATCEM.NS", "RPPINFRA.NS", "SVLL.NS",
                       "SMARTLINK.NS", "ASPINWALL.NS", "LAMBODHARA.NS", "DJML.NS", "TIL.NS", "ELGIRUBCO.NS",
                       "JAINAM.NS", "WORTH.NS", "ISFT.NS", "GINNIFILA.NS", "PILITA.NS", "SOFTTECH.NS", "DUCON.NS",
                       "VETO.NS", "RANEENGINE.NS", "AVONMORE.NS", "KBCGLOBAL.NS", "PANSARI.NS", "MODIRUBBER.NS",
                       "INVENTURE.NS", "KAPSTON.NS", "AKSHOPTFBR.NS", "JMA.NS", "EMMBI.NS", "NITCO.NS", "IRIS.NS",
                       "SHERA.NS", "DRSDILIP.NS", "UNITEDTEA.NS", "JOCIL.NS", "MANAKALUCO.NS", "VIPULLTD.NS",
                       "SIKKO.NS", "GILLANDERS.NS", "SVPGLOB.NS", "VISASTEEL.NS", "DCM.NS", "INTENTECH.NS",
                       "TEXMOPIPES.NS", "WEIZMANIND.NS", "BYKE.NS", "RAJSREESUG.NS", "ZODIAC.NS", "ARSHIYA.NS",
                       "UMANGDAIRY.NS", "LOVABLE.NS", "HOMESFY.NS", "ALPHAGEO.NS", "NDGL.NS", "PRAXIS.NS",
                       "ARTNIRMAN.NS", "SHIGAN.NS", "NOIDATOLL.NS", "UMAEXPORTS.NS", "VELS.NS", "ATLANTA.NS",
                       "MOTOGENFIN.NS", "AVROIND.NS", "SALONA.NS", "INDIANCARD.NS", "SPTL.NS", "PRITIKAUTO.NS",
                       "URAVI.NS", "IVP.NS", "MAHAPEXLTD.NS", "SOMATEX.NS", "LEXUS.NS", "WANBURY.NS", "LOTUSEYE.NS",
                       "KREBSBIO.NS", "RNAVAL.NS", "WSI.NS", "RHFL.NS", "HDIL.NS", "DCI.NS", "RVHL.NS", "XELPMOC.NS",
                       "RKEC.NS", "RELCHEMQ.NS", "DIL.NS", "ATALREAL.NS", "KOHINOOR.NS", "SALSTEEL.NS", "A2ZINFRA.NS",
                       "TARACHAND.NS", "INDOWIND.NS", "BLBLIMITED.NS", "FRETAIL.NS", "ROML.NS", "SURANAT&P.NS",
                       "ALPA.NS", "SUNDRMBRAK.NS", "PARIN.NS", "NILASPACES.NS", "AHLADA.NS", "MAGNUM.NS",
                       "REMSONSIND.NS", "STARTECK.NS", "BOHRAIND.NS", "COMPINFO.NS", "CORALFINAC.NS", "MRO-TEK.NS",
                       "SECURKLOUD.NS", "ZEELEARN.NS", "SADBHIN.NS", "BALPHARMA.NS", "NIRAJ.NS", "GSTL.NS", "OBCL.NS",
                       "TAINWALCHM.NS", "ARCHIDPLY.NS", "JHS.NS", "SITINET.NS", "MUKTAARTS.NS", "CMNL.NS",
                       "GAYAPROJ.NS", "AKG.NS", "FCONSUMER.NS", "PALASHSECU.NS", "CCHHL.NS", "SIGIND.NS", "AIROLAM.NS",
                       "WELINV.NS", "LEMERITE.NS", "CTE.NS", "UNIVASTU.NS", "SUNDARAM.NS", "MANAKCOAT.NS", "ARVEE.NS",
                       "SECURCRED.NS", "ASTRON.NS", "FLFL.NS", "STEELCITY.NS", "LLOYDS.NS", "GANGESSECU.NS",
                       "INDBANK.NS", "SUMIT.NS", "FIBERWEB.NS", "ALKALI.NS", "LASA.NS", "JAIPURKURT.NS", "MHHL.NS",
                       "BAHETI.NS", "DGCONTENT.NS", "VMARCIND.NS", "PKTEA.NS", "DAMODARIND.NS", "NECCLTD.NS",
                       "CAPTRUST.NS", "MITCON.NS", "TIRUPATIFL.NS", "IL&FSTRANS.NS", "SRPL.NS", "SURYALAXMI.NS",
                       "CEREBRAINT.NS", "KSHITIJPOL.NS", "LAGNAM.NS", "ANLON.NS", "AMJLAND.NS", "BINANIIND.NS",
                       "PROLIFE.NS", "INCREDIBLE.NS", "SHAHALLOYS.NS", "AMDIND.NS", "OMAXAUTO.NS", "TOKYOPLAST.NS",
                       "GROBTEA.NS", "ANIKINDS.NS", "SURANASOL.NS", "FIDEL.NS", "MAHASTEEL.NS", "AURDIS.NS",
                       "SIMBHALS.NS", "GAL.NS", "GICL.NS", "KALYANIFRG.NS", "HINDCON.NS", "CORDSCABLE.NS", "YAARI.NS",
                       "SONAMCLOCK.NS", "MAHICKRA.NS", "HPIL.NS", "LPDC.NS", "DBSTOCKBRO.NS", "AUSOMENT.NS",
                       "BALLARPUR.NS", "AVSL.NS", "SPMLINFRA.NS", "BANKA.NS", "GOLDENTOBC.NS", "GTL.NS", "ENERGYDEV.NS",
                       "PANACHE.NS", "PIGL.NS", "DELTAMAGNT.NS", "SHRADHA.NS", "PIONEEREMB.NS", "GLOBALVECT.NS",
                       "BAGFILMS.NS", "WIPL.NS", "NITIRAJ.NS", "BEARDSELL.NS", "KRITIKA.NS", "PATINTLOG.NS", "SETCO.NS",
                       "PRAENG.NS", "ELECTHERM.NS", "UCL.NS", "PRAKASHSTL.NS", "CINEVISTA.NS", "SUULD.NS",
                       "FLEXITUFF.NS", "MDL.NS", "HISARMETAL.NS", "SUVIDHAA.NS", "BIOFILCHEM.NS", "MARSHALL.NS",
                       "ARIHANTACA.NS", "CELEBRITY.NS", "VIAZ.NS", "DHRUV.NS", "CENTEXT.NS", "DOLLEX.NS", "BHANDARI.NS",
                       "TREJHARA.NS", "FELIX.NS", "NGIL.NS", "SUPREMEINF.NS", "AGROPHOS.NS", "MCL.NS", "OILCOUNTUB.NS",
                       "UMA.NS", "MORARJEE.NS", "SRIVASAVI.NS", "AAREYDRUGS.NS", "AAKASH.NS", "VASWANI.NS",
                       "KANANIIND.NS", "ARCHIES.NS", "SHIVAMILLS.NS", "IPSL.NS", "TREEHOUSE.NS", "BDR.NS",
                       "VERTEXPLUS.NS", "KEYFINSERV.NS", "KHFM.NS", "AROGRANITE.NS", "SEYAIND.NS", "GIRIRAJ.NS",
                       "RSSOFTWARE.NS", "ORIENTLTD.NS", "EXCEL.NS", "RELIABLE.NS", "AAATECH.NS", "AGRITECH.NS",
                       "LGHL.NS", "SHRENIK.NS", "ANKITMETAL.NS", "JETFREIGHT.NS", "VARDMNPOLY.NS", "NIRMAN.NS",
                       "SHREERAMA.NS", "SIDDHIKA.NS", "BVCL.NS", "KKVAPOW.NS", "HOVS.NS", "AMBANIORG.NS", "FSC.NS",
                       "ABMINTLLTD.NS", "SEPOWER.NS", "BANARBEADS.NS", "REGENCERAM.NS", "PODDARHOUS.NS", "PENTAGOLD.NS",
                       "PARTYCRUS.NS", "SONAHISONA.NS", "MALUPAPER.NS", "MOKSH.NS", "PULZ.NS", "RBMINFRA.NS",
                       "ZENITHSTL.NS", "NIDAN.NS", "SAMBHAAV.NS", "UWCSL.NS", "BANG.NS", "MRO.NS", "MINDPOOL.NS",
                       "TAPIFRUIT.NS", "ABCOTS.NS", "PNC.NS", "SURANI.NS", "PRECISION.NS", "TIMESGTY.NS",
                       "MANUGRAPH.NS", "ZENITHEXPO.NS", "AARVEEDEN.NS", "SOMICONVEY.NS", "DKEGL.NS", "ARHAM.NS",
                       "TIMESCAN.NS", "SGL.NS", "WEWIN.NS", "CMRSL.NS", "SONUINFRA.NS", "VIVIANA.NS", "AKASH.NS",
                       "INDSWFTLTD.NS", "KARMAENG.NS", "NAGREEKEXP.NS", "BURNPUR.NS", "NIBL.NS", "CUBEXTUB.NS",
                       "AISL.NS", "SHAIVAL.NS", "VINEETLAB.NS", "ARISTO.NS", "TERASOFT.NS", "CROWN.NS", "JFLLIFE.NS",
                       "GLOBE.NS", "3PLAND.NS", "VERA.NS", "MILTON.NS", "ADROITINFO.NS", "SHUBHLAXMI.NS", "AGNI.NS",
                       "LFIC.NS", "VSCL.NS", "MADHAV.NS", "UJAAS.NS", "SUPERSPIN.NS", "RKDL.NS", "AMBICAAGAR.NS",
                       "ACEINTEG.NS", "OMFURN.NS", "SWARAJ.NS", "AJOONI.NS", "KHANDSE.NS", "SAGARDEEP.NS",
                       "REXPIPES.NS", "ADL.NS", "MCON.NS", "CADSYS.NS", "HBSL.NS", "SANGINITA.NS", "GANGAFORGE.NS",
                       "ABINFRA.NS", "PERFECT.NS", "NARMADA.NS", "RMDRIP.NS", "NAGREEKCAP.NS", "LAXMICOT.NS",
                       "PEARLPOLY.NS", "HECPROJECT.NS", "SANWARIA.NS", "MEGAFLEX.NS", "GISOLUTION.NS", "PARASPETRO.NS",
                       "RITEZONE.NS", "HEADSUP.NS", "VCL.NS", "PRITIKA.NS", "KEEPLEARN.NS", "COUNCODOS.NS", "ROLTA.NS",
                       "DHARSUGAR.NS", "ASLIND.NS", "AGARWALFT.NS", "NEXTMEDIA.NS", "RICHA.NS", "DNAMEDIA.NS",
                       "AMEYA.NS", "DYNAMIC.NS", "LIBAS.NS", "JETKNIT.NS", "BALKRISHNA.NS", "MTEDUCARE.NS", "GODHA.NS",
                       "GOENKA.NS", "HAVISHA.NS", "QUADPRO.NS", "QFIL.NS", "MADHUCON.NS", "ROLLT.NS", "CYBERMEDIA.NS",
                       "JAKHARIA.NS", "VEEKAYEM.NS", "TGBHOTELS.NS", "VIVIDHA.NS", "FMNL.NS", "WALPAR.NS", "DESTINY.NS",
                       "SUMEETINDS.NS", "ICDSLTD.NS", "LRRPL.NS", "MPTODAY.NS", "21STCENMGM.NS", "HYBRIDFIN.NS",
                       "SABAR.NS", "TFL.NS", "IMPEXFERRO.NS", "INFOMEDIA.NS", "NKIND.NS", "SHANTI.NS", "GRCL.NS",
                       "FEL.NS", "THOMASCOTT.NS", "KHAITANLTD.NS", "WILLAMAGOR.NS", "LCCINFOTEC.NS", "UNIINFO.NS",
                       "ASMS.NS", "VIVO.NS", "GAYAHWS.NS", "CALSOFT.NS", "MOXSH.NS", "ORIENTALTL.NS", "ONELIFECAP.NS",
                       "VIJIFIN.NS", "DIGJAMLMTD.NS", "KRIDHANINF.NS", "SILLYMONKS.NS", "MAKS.NS", "TANTIACONS.NS",
                       "SUPREMEENG.NS", "SILGO.NS", "MOHITIND.NS", "EDUCOMP.NS", "EASTSILK.NS", "KANDARP.NS",
                       "CMICABLES.NS", "NATNLSTEEL.NS", "MITTAL.NS", "SPRL.NS", "ORTINLAB.NS", "BRIGHT.NS",
                       "KAUSHALYA.NS", "GUJRAFFIA.NS", "MASKINVEST.NS", "ISHAN.NS", "CONTI.NS", "AMIABLE.NS",
                       "AILIMITED.NS", "EUROTEXIND.NS", "TIJARIA.NS", "TNTELE.NS", "KALYANI.NS", "SETUINFRA.NS",
                       "GRETEX.NS", "LYPSAGEMS.NS", "METALFORGE.NS", "SSINFRA.NS", "SMVD.NS", "RMCL.NS", "JALAN.NS",
                       "SANCO.NS", "VASA.NS", "KAVVERITEL.NS", "TECHIN.NS", "NORBTEAEXP.NS", "KCK.NS", "SPENTEX.NS",
                       "CREATIVEYE.NS", "ANTGRAPHIC.NS", "TVVISION.NS", "ABNINT.NS", "ARENTERP.NS", "UMESLTD.NS",
                       "SHYAMTEL.NS", "MANAV.NS", "ACCORD.NS", "DRL.NS", "GLFL.NS", "CMMIPL.NS", "NIRAJISPAT.NS",
                       "DCMFINSERV.NS", "SRIRAM.NS", "PREMIER.NS", "SKSTEXTILE.NS", "SABTN.NS", "TARAPUR.NS",
                       "BKMINDST.NS", "ALPSINDUS.NS", "AHIMSA.NS", "BHALCHANDR.NS", "INNOVATIVE.NS", "LAKPRE.NS",
                       "TRANSWIND.NS", "MELSTAR.NS", "SABEVENTS.NS", "INDLMETER.NS", "TECILCHEM.NS"]

    return full_stock_list


def get_stock_list():
    stock_list = si.tickers_nifty50()
    return stock_list


def calculate_rsi(data, period=14):
    # Calculate price changes
    delta = data.diff(1)

    # Calculate gains (positive changes) and losses (negative changes)
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    # Calculate average gains and losses over the specified period
    avg_gain = gains.rolling(window=period, min_periods=1).mean()
    avg_loss = losses.rolling(window=period, min_periods=1).mean()

    # Calculate the relative strength (RS)
    rs = avg_gain / avg_loss

    # Calculate the relative strength index (RSI)
    rsi = 100 - (100 / (1 + rs))

    return rsi


class MACross(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._trade_data = {}

    def get(self, request):
        try:
            params = request.query_params
            symbol = params.get("Stock")
            short_window = int(params.get("ShortWindow"))
            long_window = int(params.get("LongWindow"))
            start_date = params.get("StartDate")
            end_date = params.get("EndDate", datetime.date.today())
            plot = params.get("Plot", False)
            detail = params.get("Detail", False) if params.get("Detail", False) == "True" else False
            self.plot_moving_average_crossover(symbol, short_window, long_window, start_date, end_date, plot, detail)
        except Exception as e:
            print(e, "error in main func.")
        while self._trade_data is None:
            time.sleep(1)
        response = {"code": 200, "status": "success", "data": self._trade_data}
        return Response(response)

    def plot_moving_average_crossover(self, symbol, short_window, long_window, start_date, end_date, plot, detail):
        # Get stock data
        try:
            # get_stock_symbol()
            try:
                stock_data = get_stock_data(symbol, start_date, end_date)
                stock_data.dropna()
                stock_info = get_stock_info(symbol)
                r_data = {}
                if stock_info:
                    if detail:
                        r_keys = get_req_data_keys()
                        for key in r_keys:
                            r_data.setdefault(key, stock_info.info.get(key))
                r_data.setdefault("currentPrice", stock_info.info.get("currentPrice"))
                self._trade_data.setdefault(symbol, {}).update(r_data)
                # Calculate short and long-term moving averages
                # Example usage:
                # Assuming you have a DataFrame 'df' with a column 'Close' representing closing prices
                # and you want to calculate RSI for a 14-day period
                # Add RSI column to the DataFrame
                rsi = calculate_rsi(stock_data, period=14)
                rsi.dropna()
                print(rsi)
                short_rolling = stock_data.rolling(window=short_window).mean()
                long_rolling = stock_data.rolling(window=long_window).mean()

                # Plotting
                if plot:
                    plt.figure(figsize=(120, 8))
                    plt.title(f'{symbol} Moving Average Crossover')
                    plt.plot(stock_data, label='Close Price', color='blue')
                    plt.plot(short_rolling, label=f'{short_window}-day SMA', color='orange')
                    plt.plot(long_rolling, label=f'{long_window}-day SMA', color='green')
                    manager = plt.get_current_fig_manager()
                    manager.full_screen_toggle()
                # Plot Buy and Sell signals
                buy_signal = short_rolling[short_rolling > long_rolling]
                sell_signal = short_rolling[short_rolling <= long_rolling]
                # Calculate RSI
                rsi_data = {"date": rsi.index[-1], "price": rsi.values[-1]} if len(
                    rsi.index) > 0 else {}
                self._trade_data.setdefault(symbol, {}).update({
                    "rsi": rsi_data})
                buy_data = {"date": buy_signal.index[-1], "price": buy_signal.values[-1]} if len(
                    buy_signal.index) > 0 else {}
                self._trade_data.setdefault(symbol, {}).update({
                    "buy_signal": buy_data})
                sell_data = {"date": sell_signal.index[-1], "price": sell_signal.values[-1]} if len(
                    sell_signal.index) > 0 else {}
                self._trade_data.setdefault(symbol, {}).update({"sell_signal": sell_data})
                if plot:
                    plt.scatter(buy_signal.index, buy_signal, label='Buy Signal', marker='^', color='green')
                    plt.scatter(sell_signal.index, sell_signal, label='Sell Signal', marker='v', color='red')
                    plt.xlabel('Date')
                    plt.ylabel('Close Price')
                    plt.legend()
                    plt.show()
            except Exception as e:
                self._trade_data[symbol] = {"error": str(e)}

        except Exception as e:
            self._trade_data = str(e)


class MACrossMulti(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._trade_data = {}

    def get(self, request):
        try:
            params = request.query_params
            short_window = int(params.get("ShortWindow"))
            long_window = int(params.get("LongWindow"))
            start_date = params.get("StartDate")
            end_date = params.get("EndDate", datetime.date.today())
            detail = params.get("Detail", False) if params.get("Detail", False) == "True" else False
            self.plot_moving_average_crossover(short_window, long_window, start_date, end_date, detail)
        except Exception as e:
            print(e, "error in main func.")
        while self._trade_data is None:
            time.sleep(1)
        response = {"code": 200, "status": "success", "data": self._trade_data}
        return Response(response)

    def plot_moving_average_crossover(self, short_window, long_window, start_date, end_date, detail):
        # Get stock data
        try:
            stock_err = []
            stock_list = get_all_stocks()
            for stock in stock_list:
                try:
                    stock_data = get_stock_data(stock, start_date, end_date)
                    stock_data.dropna()
                    stock_info = get_stock_info(stock)
                    r_data = {}
                    if stock_info:
                        if detail:
                            r_keys = get_req_data_keys()
                            for key in r_keys:
                                r_data.setdefault(key, stock_info.info.get(key))
                    r_data.setdefault("currentPrice", stock_info.info.get("currentPrice"))
                    self._trade_data.setdefault(stock, {}).update(r_data)
                    rsi = calculate_rsi(stock_data, period=14)
                    rsi.dropna()
                    short_rolling = stock_data.rolling(window=short_window).mean()
                    long_rolling = stock_data.rolling(window=long_window).mean()

                    # Plot Buy and Sell signals
                    buy_signal = short_rolling[short_rolling > long_rolling]
                    sell_signal = short_rolling[short_rolling <= long_rolling]
                    # Calculate RSI
                    rsi_data = {"date": rsi.index[-1], "price": rsi.values[-1]} if len(
                        rsi.index) > 0 else {}
                    self._trade_data.setdefault(stock, {}).update({
                        "rsi": rsi_data})
                    buy_data = {"date": buy_signal.index[-1], "price": buy_signal.values[-1]} if len(
                        buy_signal.index) > 0 else {}
                    if buy_data.get("price"):
                        price_diff = ((buy_signal.values[-1] - stock_info.info.get("currentPrice")) / buy_signal.values[
                            -1]) * 100
                        self._trade_data.setdefault(stock, {}).update({
                            "buy price diff": price_diff})
                    self._trade_data.setdefault(stock, {}).update({
                        "buy_signal": buy_data})
                    sell_data = {"date": sell_signal.index[-1], "price": sell_signal.values[-1]} if len(
                        sell_signal.index) > 0 else {}
                    self._trade_data.setdefault(stock, {}).update({"sell_signal": sell_data})
                except Exception as e:
                    stock_err.append(stock)
                    self._trade_data[stock] = {"error": str(e)}
            print(stock_err)
        except Exception as e:
            self._trade_data = str(e)


class MACrossFilter(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._trade_data = {}

    def get(self, request):
        try:
            params = request.query_params
            short_window = int(params.get("ShortWindow"))
            long_window = int(params.get("LongWindow"))
            start_date = params.get("StartDate")
            end_date = params.get("EndDate", datetime.date.today())
            detail = params.get("Detail", False) if params.get("Detail", False) == "True" else False
            self.plot_moving_average_crossover(short_window, long_window, start_date, end_date, detail)
        except Exception as e:
            print(e, "error in main func.")
        while self._trade_data is None:
            time.sleep(1)
        response = {"code": 200, "status": "success", "data": self._trade_data}
        return Response(response)

    def plot_moving_average_crossover(self, short_window, long_window, start_date, end_date, detail):
        # Get stock data
        try:
            stock_list = get_stock_list()
            for stock in stock_list:
                try:
                    stock_data = get_stock_data(stock, start_date, end_date)
                    stock_info = get_stock_info(stock)
                    r_data = {}
                    if stock_info:
                        if detail:
                            r_keys = get_req_data_keys()
                            for key in r_keys:
                                r_data.setdefault(key, stock_info.info.get(key))
                    r_data.setdefault("currentPrice", stock_info.info.get("currentPrice"))
                    self._trade_data.setdefault(stock, {}).update(r_data)
                    short_rolling = stock_data.rolling(window=short_window).mean()
                    long_rolling = stock_data.rolling(window=long_window).mean()
                    # Calculate RSI
                    rsi = calculate_rsi(stock_data, period=14)
                    # Plot Buy and Sell signals
                    buy_signal = short_rolling[short_rolling > long_rolling]
                    sell_signal = short_rolling[short_rolling <= long_rolling]
                    rsi_data = {"date": rsi.index[-1], "price": rsi.values[-1]} if len(
                        rsi.index) > 0 else {}
                    self._trade_data.setdefault(stock, {}).update({
                        "rsi": rsi_data})
                    buy_data = {"date": buy_signal.index[-1], "price": buy_signal.values[-1]} if len(
                        buy_signal.index) > 0 else {}
                    self._trade_data.setdefault(stock, {}).update({
                        "buy_signal": buy_data})
                    sell_data = {"date": sell_signal.index[-1], "price": sell_signal.values[-1]} if len(
                        sell_signal.index) > 0 else {}
                    self._trade_data.setdefault(stock, {}).update({"sell_signal": sell_data})
                except Exception as e:
                    self._trade_data[stock] = {"error": str(e)}

        except Exception as e:
            self._trade_data = str(e)
