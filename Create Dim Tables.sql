/****** Script for SelectTopNRows command from SSMS  ******/

-- Step One - Create pid -> Product Mapping

	-- Substep One - Get distinct list of Product Names

		select distinct [Product] 
		into #tmp_Product
		from  [dbo].[BaseData]

-- Substep Two - Create pid

       drop table if exists #Product

              select row_number() over (order by A.[Product]) as [pid],
                       A.[Product] as [pname]
              into #tmp_Product_Mapping

              from #tmp_Product A

-- Step Two - Create Covers Table

		SELECT distinct c.[pid],
					A.[drg_cd]

		into #covers
		FROM [dbo].[BaseData] A

		left join [dbo].[MCO] B
		on A.[MCO] = B.[mname]

		left join #tmp_Product_Mapping C --Edited from #tmp_Product_Mapping to #tmp_Product
		on A.[Product] = C.[pname]

		order by c.[pid], [drg_cd]

-- Step Three - Create Offers 
		
		SELECT distinct b.[mid],
						c.[pid]
		into #offers
		FROM [dbo].[BaseData] A

		left join [dbo].[MCO] B
		on A.[MCO] = B.[mname]

		left join #tmp_Product_Mapping C
		on A.[Product] = C.[pname]


		order by c.[pid], [drg_cd]

-- Step Four - Create Costs Table

		SELECT H.[hid],
			   A.[drg_cd],
			   P.[pid],
			   A.[Charge] as [allowed]

	    into #Costs
		FROM [dbo].[BaseData] A

		left join [dbo].[Hospital] H
		on A.[Hospital] = H.[hname]

		left join #tmp_Product_Mapping P
		on A.[Product] = P.[pname]

-- Step Five - Create Service

		-- Substep One - Unique combinations of drg_cd and drg_desc (will have multiple drg_descriptions per drg_cd)
		
			select distinct A.[drg_cd],
							A.[drg_desc]
			into #tmp_Service_01
			from [dbo].[BaseData] A

			order by A.[drg_cd]

		-- Substep Two - Create a row number for each DRG_Code. Will select instances where its 1.

			select row_number() over (partition by A.[drg_cd] order by A.[drg_cd]) as [Id],
				 A.[drg_cd], 
					A.[drg_desc]
			into #tmp_Service_02 
			from #tmp_Service_01 A

		-- Substpe Three - Create Services table

			select A.[drg_cd], A.[drg_desc]
			into #Services
			from #tmp_Service_02 A where A.[id] = 1

-- Step Five - Create Provides

		select distinct H.[hid],
						A.[drg_cd],
						A.[Hospital]

		FROM [dbo].[BaseData] A

		left join [dbo].[Hospital] H
		on A.[Hospital] = H.[hname]
