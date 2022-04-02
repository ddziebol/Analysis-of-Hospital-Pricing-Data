drop table if exists BaseData

SELECT E.Hospital, E.drg_cd, E.drg_desc, E.Provider as MCO, E.Product, case when E.charge = '#VALUE!' then 0 when E.Charge = '889 per diem' then 0 else cast(E.Charge as money) end as Charge INTO dbo.BaseData FROM dbo.Essentia2 E
UNION
SELECT M.Hospital, M.drg_cd, M.drg_desc, M.MCO, M.Product, cast(M.Gross_Nominal_Charge as money) as Charge FROM dbo.Mayo M
UNION 
SELECT   F.Hospital, right(F.Code_Num,3) as drg_cd , F.[Desc] as drg_desc, F.Provider as MCO, F.Product, case when F.IPRate = 'NA' then 0 else cast(F.IPRate as float) end as Charge FROM [dbo].[Fairview3] F where F.Code_Type LIKE '%MS%'

SELECT DISTINCT F.IPRate FROM dbo.Fairview3 F order by F.IPRate
--LEFT JOIN dbo.Hospital H
--ON E.Hospital = H.hname
--LEFT JOIN dbo.Product P 
--ON P.pname = H.Product