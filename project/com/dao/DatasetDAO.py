from project import db
from project.com.vo.DatasetVO import DatasetVO


class DatasetDAO:
    def insertDataset(self, datasetVO):
        db.session.add(datasetVO)
        db.session.commit()

    def viewDataset(self):
        datasetList = DatasetVO.query.all()

        return datasetList

    def deleteDataset(self, datasetVO):
        datasetList = DatasetVO.query.get(datasetVO.datasetId)

        db.session.delete(datasetList)

        db.session.commit()
        return  datasetList

        # def editCategory(self, categoryVO):
        #     # categoryList = CategoryVO.query.get(categoryVO.categoryId)
        #
        #     # categoryList = CategoryVO.query.filter_by(categoryId=categoryVO.categoryId)
        #
        #     categoryList = CategoryVO.query.filter_by(categoryId=categoryVO.categoryId).all()
        #
        #     return categoryList
        #
        # def updateCategory(self, categoryVO):
        #     db.session.merge(categoryVO)
        #
        #     db.session.commit()
