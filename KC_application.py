from asyncio.windows_events import NULL
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "451Project.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Milestone1(QMainWindow):
    def __init__(self):
        super(Milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.loadCategories()
        self.loadBusinesses()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChange)
        self.ui.zipcodeList.itemSelectionChanged.connect(self.zipcodeChange)
        self.ui.businessSearch.textChanged.connect(self.searchBusiness)
        self.ui.categoryList.itemSelectionChanged.connect(self.categoryChange)
        self.ui.pushButton.clicked.connect(self.clearCategories)

    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='Ss329676**'")
        except:
            print('Unable to connect to database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        results = cur.fetchall()
        conn.close()
        return results
    
    def clearStats(self):
        self.ui.populationCount.clear()
        self.ui.businessCount.clear()
        self.ui.AverageIncome.clear()
        self.ui.popularList.clear()
        self.ui.successfulList.clear()
        self.ui.popularList.setRowCount(1)
        self.ui.successfulList.setRowCount(1)
        self.ui.tableWidget.setRowCount(0)
    
    def clearCategories(self):
        self.ui.categoryList.clear()
        self.loadCategories()
        if(self.ui.stateList.currentIndex() >= 0):
            state = self.ui.stateList.currentText()
            sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                  WHERE business.business_id = category.business_id and\
                      state = '"+ state +"' ORDER BY name;"
                
            if(len(self.ui.cityList.selectedItems()) > 0):
                city = self.ui.cityList.selectedItems()[0].text()
                sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                            WHERE business.business_id = category.business_id and\
                            state = '"+ state +"' and city = '"+ city +"' ORDER BY name;"
                    
                if len(self.ui.zipcodeList.selectedItems()) > 0:
                    zipcode = self.ui.zipcodeList.selectedItems()[0].text()
                    sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                            WHERE business.business_id = category.business_id  and\
                            state = '"+ state +"' and city = '"+ city +"' AND zipcode = '"+ zipcode +"' ORDER BY name;"
        else:
            sql_str = "select distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business ORDER BY name;"
        self.loadBusinessTable(sql_str)

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct State FROM BUSINESS ORDER BY State;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query Failed")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def loadCategories(self):
        self.ui.categoryList.clear()
        sql_str = "select distinct category_name from category order by category_name"

        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.categoryList.addItem(row[0])
        except:
            print("Query Failed")

    def categoryChange(self):
        if len(self.ui.categoryList.selectedItems()) > 0:
            category = self.ui.categoryList.selectedItems()[0].text()
        else:
            self.loadBusinesses()
            return
        
        if(self.ui.stateList.currentIndex() >= 0):
            state = self.ui.stateList.currentText()
            sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                  WHERE business.business_id = category.business_id and category_name = '" + category + "' and\
                      state = '"+ state +"' ORDER BY name;"
            if(len(self.ui.cityList.selectedItems()) > 0):
                city = self.ui.cityList.selectedItems()[0].text()
                sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                            WHERE business.business_id = category.business_id and category_name = '" + category + "' and\
                            state = '"+ state +"' and city = '"+ city +"' ORDER BY name;"
                if len(self.ui.zipcodeList.selectedItems()) > 0:
                    zipcode = self.ui.zipcodeList.selectedItems()[0].text()
                    sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                            WHERE business.business_id = category.business_id and category_name = '" + category + "' and\
                            state = '"+ state +"' and city = '"+ city +"' AND zipcode = '"+ zipcode +"' ORDER BY name;"
        else:
            sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                WHERE business.business_id = category.business_id and category_name =  '" + category + "' ORDER BY name;"
        self.loadBusinessTable(sql_str)

    def loadBusinessTable(self, sql):
        try:
            results = self.executeQuery(sql)
            if results == NULL:
                print("NO")
            #print(results)
            style = "::section{""background-color: rgb(200,200,200);}"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.verticalHeader().setStyleSheet(style)
            self.ui.businessTable.setColumnCount(len(results[0]))
            self.ui.businessTable.setRowCount(len(results))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Stars','Review\n Count', "Review\n Rating",
                                                              "Number of\n Checkins"])
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0, 285)
            self.ui.businessTable.setColumnWidth(1, 100)
            self.ui.businessTable.setColumnWidth(5, 70)
            currentRowCount = 0
            for row in results:
                for colCount in range(0,len(results[0])):
                    self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
        except:
            self.ui.businessTable.clear()
            self.ui.businessTable.setRowCount(1)
            #self.ui.businessTable.setColumnWidth(0, 305)
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Stars','Review\n Count', "Review\n Rating",
                                                              "Number of\n Checkins"])
            print("Query Failed")
        self.ui.businessTable.verticalHeader().setVisible(False)
        
    def loadBusinesses(self):
        sql_str = f"select distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business ORDER BY name;"
        self.loadBusinessTable(sql_str)

    def stateChanged(self):
        self.clearStats()
        self.ui.businessCount.clear()
        self.ui.populationCount.clear()
        self.ui.AverageIncome.clear()
        self.ui.cityList.clear()
        self.ui.zipcodeList.clear()
        self.ui.businessSearch.clear()
        state = self.ui.stateList.currentText()
        sql_str = "SELECT distinct city FROM business where state = '" + state + "'ORDER BY city;"
        if (self.ui.stateList.currentIndex()>=0):
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query Failed")

        sql_str = "SELECT distinct Zipcode FROM business where state = '" + state + "' ORDER BY Zipcode;"
        if (self.ui.stateList.currentIndex()>=0):
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipcodeList.addItem(str(row[0]))
            except:
                print("Query Failed")
        
        if len(self.ui.categoryList.selectedItems()) > 0:
            category = self.ui.categoryList.selectedItems()[0].text()
            sql_str = sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                  WHERE business.business_id = category.business_id and category_name =  '" + category + "' and\
                      state = '"+ state +"' ORDER BY name;"
        else:
            sql_str = f"SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business WHERE state = '{state}' ORDER BY name;"
        self.loadBusinessTable(sql_str)

    def cityChange(self):
          self.clearStats()
          self.ui.zipcodeList.clear()
          self.ui.businessSearch.clear()
          if ((self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0)):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()

         
            sql_str = "SELECT distinct Zipcode FROM business where city = '" + city + "' ORDER BY Zipcode;"
            if (self.ui.stateList.currentIndex()>=0):
                try:
                    results = self.executeQuery(sql_str)
                    for row in results:
                        self.ui.zipcodeList.addItem(str(row[0]))
                except:
                    print("Query Failed")

            if len(self.ui.categoryList.selectedItems()) > 0:
                category = self.ui.categoryList.selectedItems()[0].text()
                sql_str = sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                  WHERE business.business_id = category.business_id and category_name =  '" + category + "' and\
                      state = '"+ state +"' AND city = '"+ city +"' ORDER BY name;"
                
            else:
                sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business WHERE state = '" + state + "' AND city='" + city + "' \
                    ORDER BY name;"
            self.loadBusinessTable(sql_str)

    def zipcodeChange(self):

        self.ui.businessSearch.clear()
        state = self.ui.stateList.currentText()
        if ((self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and len(self.ui.zipcodeList.selectedItems()) > 0):
            city = self.ui.cityList.selectedItems()[0].text()
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()
            self.setBusinessCount()
            self.setPopulation()
            self.setAverageIncome()
            self.loadPopular()
            self.loadSuccesful()
            self.loadPopularCategories()

            if len(self.ui.categoryList.selectedItems()) > 0:
                category = self.ui.categoryList.selectedItems()[0].text()
                sql_str = sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                  WHERE business.business_id = category.business_id and category_name =  '" + category + "' and\
                      state = '"+ state +"' AND city = '"+ city +"'  AND zipcode = '"+ zipcode +"' ORDER BY name;"
            else:
                sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business WHERE state = '" + state + "' AND city='" + city + "'\
                    AND zipcode = '" + zipcode + "' ORDER BY name;"
            self.loadBusinessTable(sql_str)

    def searchBusiness(self):
        businessName = self.ui.searchBox.text() 

        if(self.ui.stateList.currentIndex() >= 0):
            state = self.ui.stateList.currentText()
            sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business WHERE name like '%" + businessName + "%'\
                  AND state='"+ state +"' ORDER BY name"

            if(len(self.ui.cityList.selectedItems()) > 0):
               city = self.ui.cityList.selectedItems()[0].text() 
               sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business WHERE name like '%" + businessName + "%'\
                  AND state='"+ state +"' AND city='" + city +"' ORDER BY name"

               if len(self.ui.zipcodeList.selectedItems()) > 0:
                   zipcode = self.ui.zipcodeList.selectedItems()[0].text()
                   sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business WHERE name like '%" + businessName + "%'\
                      AND state='"+ state +"' AND city='" + city +"' AND zipcode = '" + zipcode +"' ORDER BY name"
            
            elif len(self.ui.zipcodeList.selectedItems()) > 0:
                zipcode = self.ui.zipcodeList.selectedItems()[0].text()
                sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business WHERE name like '%" + businessName + "%'\
                      AND state='"+ state +"' AND zipcode = '" + zipcode +"' ORDER BY name"
                
        elif len(self.ui.categoryList.selectedItems()) > 0:
            category = self.ui.categoryList.selectedItems()[0].text()
            sql_str ="SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business WHERE name like '%" + businessName + "%'\
                  AND category_name = '"+ category +"' ORDER BY name"

            if(self.ui.stateList.currentIndex() >= 0):
                state = self.ui.stateList.currentText()
                sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                  WHERE name like '%" + businessName + "%' and business.business_id = category.business_id and category_name =  '" + category + "' and\
                      state = '"+ state +"' ORDER BY name;"
                
                if(len(self.ui.cityList.selectedItems()) > 0):
                    city = self.ui.cityList.selectedItems()[0].text()
                    sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                            WHERE name like '%" + businessName + "%' and business.business_id = category.business_id and category_name =  '" + category + "' and\
                            state = '"+ state +"' and city = '"+ city +"' ORDER BY name;"
                    
                    if len(self.ui.zipcodeList.selectedItems()) > 0:
                        zipcode = self.ui.zipcodeList.selectedItems()[0].text()
                        sql_str = "SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business, category\
                            WHERE name like '%" + businessName + "%' and business.business_id = category.business_id and category_name =  '" + category + "' and\
                            state = '"+ state +"' and city = '"+ city +"' AND zipcode = '"+ zipcode +"' ORDER BY name;"

        else:
            sql_str ="SELECT distinct name, city, state, stars, review_count, review_rating, checkin_count FROM business WHERE name like '%" + businessName + "%' ORDER BY name"

        self.loadBusinessTable(sql_str)

    def setBusinessCount(self):
        zipcode = self.ui.zipcodeList.selectedItems()[0].text()
        sql_str = "select count(business.business_id)\
                    from business, zipcode_data\
                    where zipcode_data.zipcode = '"+ zipcode +"' and business.zipcode = zipcode_data.zipcode"
        try:
            result = self.executeQuery(sql_str)
            self.ui.businessCount.setText("    " + str(result[0][0]))
        except:
            print("NO")

    def setPopulation(self):
        zipcode = self.ui.zipcodeList.selectedItems()[0].text()
        sql_str = "select distinct zipcode_data.population\
                    from business, zipcode_data\
                    where zipcode_data.zipcode = '"+ zipcode +"' and business.zipcode = zipcode_data.zipcode"
        try:
            result = self.executeQuery(sql_str)
            self.ui.populationCount.setText("    " + str(result[0][0]))
        except:
            print("NO")

    def setAverageIncome(self):
        zipcode = self.ui.zipcodeList.selectedItems()[0].text()
        sql_str = "select distinct zipcode_data.meanIncome\
                    from business, zipcode_data\
                    where zipcode_data.zipcode = '"+ zipcode +"' and business.zipcode = zipcode_data.zipcode"
        try:
            result = self.executeQuery(sql_str)
            self.ui.AverageIncome.setText("    " + str(result[0][0]))
        except:
            print("Query Failed")

    def loadPopular(self):
        zipcode = self.ui.zipcodeList.selectedItems()[0].text()
        sql_str = "select business.name, business.checkin_count, business.stars\
                    from business, zipcode_data\
                    where business.zipcode = zipcode_data.zipcode and zipcode_data.zipcode = '"+ zipcode +"' and\
                    business.checkin_count > (select avg(business.checkin_count) as reviewcount\
                    from business, zipcode_data\
                    where business.zipcode = zipcode_data.zipcode and zipcode_data.zipcode = '"+ zipcode +"') and\
                    business.review_count > (select avg(business.review_count) as reviewcount\
                    from business, zipcode_data\
                    where business.zipcode = zipcode_data.zipcode and zipcode_data.zipcode = '"+ zipcode +"')\
                    group by business.name, business.stars, business.review_rating, business.review_count, business.checkin_count"
        try:
            result = self.executeQuery(sql_str)
            style = "::section{""background-color: rgb(200,200,200);}"
            self.ui.popularList.horizontalHeader().setStyleSheet(style)
            self.ui.popularList.setColumnCount(len(result[0]))
            self.ui.popularList.setRowCount(len(result))
            self.ui.popularList.setHorizontalHeaderLabels(['Business Name', 'Check In\n Count', 'Stars'])
            self.ui.popularList.verticalHeader().setVisible(False)
            self.ui.popularList.setColumnWidth(0, 285)
            self.ui.popularList.setColumnWidth(1, 100)
            self.ui.popularList.setColumnWidth(2, 80)
            currentRowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.popularList.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
        except:
            print("Query Failed")

    def loadSuccesful(self):
        zipcode = self.ui.zipcodeList.selectedItems()[0].text()
        sql_str = "select business.name, business.stars, business.review_count\
                    from business, zipcode_data\
                    where business.zipcode = zipcode_data.zipcode and zipcode_data.zipcode = '89102' and\
                    business.stars > (select avg(business.stars) as avgstars\
                    from business, zipcode_data\
                    where business.zipcode = zipcode_data.zipcode and zipcode_data.zipcode = '"+zipcode+"') and \
                    business.review_rating > (select avg(business.review_rating) as avgreviewrating\
                    from business, zipcode_data\
                    where business.zipcode = zipcode_data.zipcode and zipcode_data.zipcode = '"+zipcode+"') and \
                    business.checkin_count > (select avg(business.checkin_count) as avgcheckins \
                    from business, zipcode_data\
                    where business.zipcode = zipcode_data.zipcode and zipcode_data.zipcode = '"+zipcode+"')\
                    group by business.name, business.stars, business.review_rating, business.review_count, business.checkin_count\
                    order by business.stars desc, business.review_rating desc, business.review_count desc, business.checkin_count desc"
        try:
            result = self.executeQuery(sql_str)
            style = "::section{""background-color: rgb(200,200,200);}"
            self.ui.successfulList.horizontalHeader().setStyleSheet(style)
            self.ui.successfulList.setColumnCount(len(result[0]))
            self.ui.successfulList.setRowCount(len(result))
            self.ui.successfulList.setHorizontalHeaderLabels(['Business Name','Stars', 'Review Count'])
            self.ui.successfulList.setColumnWidth(0, 285)
            self.ui.successfulList.setColumnWidth(1, 100)

            currentRowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.successfulList.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
            self.ui.successfulList.verticalHeader().setVisible(False)
        except:
            print("NO succ")

    def loadPopularCategories(self):
        zipcode = self.ui.zipcodeList.selectedItems()[0].text()
        sql_str = "select distinct count(category) as Number_Of_Businesses, category.category_name\
                    from zipcode_data, category, business\
                    where zipcode_data.zipcode = '"+ zipcode +"' and business.zipcode = zipcode_data.zipcode\
                    and business.business_id = category.business_id\
                    group by category.category_name\
                    order by Number_Of_Businesses desc"

        try:
            result = self.executeQuery(sql_str)

            print(result)
            style = "::section{""background-color: rgb(200,200,200);}"
            self.ui.tableWidget.horizontalHeader().setStyleSheet(style)
            self.ui.tableWidget.setColumnCount(len(result[0]))
            self.ui.tableWidget.setRowCount(len(result))
            self.ui.tableWidget.setHorizontalHeaderLabels(['Count','Category'])
            self.ui.tableWidget.setColumnWidth(0, 40)
            self.ui.tableWidget.setColumnWidth(1, 250)

            currentRowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.tableWidget.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
            self.ui.tableWidget.verticalHeader().setVisible(False)
        except:
            print("Query Failed")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Milestone1()
    window.show()
    sys.exit(app.exec_())